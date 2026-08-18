from langchain_core.documents import Document

from src.api.services.training.base_training import Training


class TrainingCourse(Training):
    def __init__(self):
        super().__init__()
        self.columns = ["title", "content", "courseid", "source", "categoryid", "categoryname"]

    def save_training_data(self, data):

        collection = self.get_collection_name(data)

        try:
            metadata = {}
            for key, value in data.items():
                if key in self.columns:
                    metadata[key] = value

            for key in self.redis_client.scan_iter(self._doc_key_pattern(collection)):
                courseid = self.redis_client.hget(key, "courseid")
                if courseid is not None and courseid.decode() == metadata["courseid"]:
                    self.redis_client.delete(key)

            document = Document(page_content=metadata["content"], metadata=metadata)

            self.vector_db.add_documents([document], collection)

            self.response["error"] = False
            self.response["message"] = "Training thành công"

            return self.response

        except Exception as e:

            print(str(e))

            self.response["error"] = True
            self.response["message"] = f"Training thất bại: {str(e)}"

            return self.response

    def delete_training_data(self, data):

        collection = self.get_collection_name(data)

        try:
            courseids_set = set(data["courseids"])
            keys_to_delete = []

            for key in self.redis_client.scan_iter(self._doc_key_pattern(collection)):
                courseid_redis = self.redis_client.hget(key, "courseid")
                if courseid_redis is not None and courseid_redis.decode() in courseids_set:
                    keys_to_delete.append(key)

            if keys_to_delete:
                self.redis_client.delete(*keys_to_delete)

            self.response["error"] = False
            self.response["message"] = "Xóa khóa học thành công"

            return self.response

        except Exception as e:

            print(str(e))
            self.response["error"] = True
            self.response["message"] = f"Xóa khóa học thất bại: {str(e)}"

            return self.response

    def check_training_duplication(self):
        pass

    def get_collection_name(self, data):
        return "course_" + data["contextdata"]["collection"]
