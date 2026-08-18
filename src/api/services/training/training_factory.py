from src.api.services.training.training_course import TrainingCourse
from src.api.services.training.training_resource import TrainingResource


class TrainingFactory:
    def create_training(self, training_type):
        if training_type == "course":
            return TrainingCourse()
        elif training_type == "resource":
            return TrainingResource()
        else:
            raise ValueError(f"Không hỗ trợ training type: {training_type}")
