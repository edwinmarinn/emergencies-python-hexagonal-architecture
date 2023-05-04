from contexts.incidents.emergencies.domain.entities.emergency import Emergency
from contexts.shared.domain.collection import Collection


class Emergencies(Collection[Emergency]):
    def type(self):
        return Emergency
