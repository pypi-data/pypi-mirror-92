from ltk.actions.action import *

class CleanAction(Action):
    def __init__(self, path):
        Action.__init__(self, path)

    def clean_action(self, force, dis_all, path):
        try:
            if dis_all:
                # disassociate everything
                self._clean_all()
                return
            if path:
                locals_to_delete = self._clean_by_path(path)
            else:
                locals_to_delete = self._check_docs_to_clean()

            # remove entry for local doc -- possibly delete local file too?
            if locals_to_delete:
                for curr_id in locals_to_delete:
                    removed_title = self._clean_local(curr_id, force)
                    logger.info('Removing association for document {0}'.format(removed_title))
            else:
                logger.info('Local documents already up-to-date with Lingotek Cloud')
                return
            logger.info('Cleaned up associations between local documents and Lingotek Cloud')
        except Exception as e:
            log_error(self.error_file_name, e)
            if 'string indices must be integers' in str(e) or 'Expecting value: line 1 column 1' in str(e):
                logger.error("Error connecting to Lingotek's TMS")
            else:
                logger.error("Error on clean: "+str(e))

    def _clean_local(self, doc_id, force):
        removed_doc = self.doc_manager.get_doc_by_prop('id', doc_id)
        if not removed_doc:
            return
        removed_title = removed_doc['name']
        if force:
            self.delete_local(removed_title, doc_id)
        self.doc_manager.remove_element(doc_id)

        return removed_title

    def _clean_by_path(self, path):
        locals_to_delete = []
        files = get_files(path)
        docs = self.doc_manager.get_file_names()
        # Efficiently go through the files in case of a large number of files to check or a large number of remote documents.
        if (files != None) and (len(files) > len(docs)):
            for file_name in docs:
                for name in files:
                    if file_name in name:
                        entry = self.doc_manager.get_doc_by_prop('file_name', self.norm_path(file_name))
                        if entry:
                            locals_to_delete.append(entry['id'])
                            self._cancel_document(entry['id'])
        elif files != None:
            for file_name in files:
                entry = self.doc_manager.get_doc_by_prop('file_name', self.norm_path(file_name))
                if entry:
                    locals_to_delete.append(entry['id'])
                    self._cancel_document(entry['id'])

        return locals_to_delete

    def _check_docs_to_clean(self):
        locals_to_delete = []
        local_ids = self.doc_manager.get_doc_ids()
        for check_id in local_ids:
            response = self.api.document_status(check_id)
            if response.status_code == 200:
                if response.json()['properties']['status'].upper() == 'CANCELLED':
                    locals_to_delete.append(check_id)
            elif response.status_code == 404:
                locals_to_delete.append(check_id)
            else:
                raise_error(response.json(), 'Error trying to list documents in TMS for cleaning')

        # check local files
        db_entries = self.doc_manager.get_all_entries()
        for entry in db_entries:
            # if local file doesn't exist, remove entry
            if not os.path.isfile(os.path.join(self.path, entry['file_name'])):
                locals_to_delete.append(entry['id'])
                self._cancel_document(entry['id'])

        return locals_to_delete

    def _clean_all(self):
        local_ids = self.doc_manager.get_doc_ids()
        for doc_id in local_ids:
            self._cancel_document(doc_id)
        self.doc_manager.clear_all()
        logger.info("Removed all associations between local and remote documents.")

    def _cancel_document(self, cancel_id):
        response = self.api.document_cancel(cancel_id)
        if response.status_code == 404 or response.status_code == 204:
            return
        if response.status_code == 400:
            for message in response.json()['messages']:
                if 'already in a completed state' in message:#currently the API response when cancelling a document that has already been cancelled or completed is "Unable to cancel documents which are already in a completed state.  Current status: COMPLETED/CANCELLED" (COMPLETED or CANCELLED, not COMPLETED/CANCELLED)
                    return
        logger.warning('Error cleaning up association in TMS for document id {0}'.format(doc_id))
