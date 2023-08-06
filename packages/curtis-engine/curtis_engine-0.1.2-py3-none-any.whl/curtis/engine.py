import os
import pickle
from .fact import CurtisFact
from .exceptions import CurtisIntegrityError


class CurtisEngine:
    """
    The Curtis engine

    This class will act as the inference engine of an expert system, in which an initial
    fact must be declared in order for curtis to run and perform a diagnosis. This fact
    must be passed as a `CurtisFact` object, that contains automatic validation for each
    expected field.
    """

    def __init__(self):
        """
        Engine constructor

        When instantiating a `CurtisEngine` object, the engine's model gets
        loaded and placed into the `engine` variable, it is necessary since 
        all classification tasks are performed by the engine.
        """
        here = os.path.dirname(os.path.abspath(__file__))

        try:
            with open(os.path.join(here, "model", "curtis.sav"), "rb") as f:
                self.engine = pickle.load(f)
        except:
            raise CurtisIntegrityError(
                "The curtis model file appears to be missing/corrupted")

    def declare_fact(self, fact: CurtisFact):
        """
        Fact declaration

        To declare a fact, a `CurtisFact` must be passed in order for the engine
        to store it, the `CurtisFact` automatically performs validation to each 
        field, making sure no value is going to affect the decision/diagnosis.

        Parameters
        ----------
        :param fact: The general fact containing a patient's ECG values

        Returns
        -------
        :return: None
        """
        self.fact = fact

    def diagnose(self):
        """
        Perform a diagnostic.

        After a fact is declared, the engine now performs a diagnostic over the
        provided values, which get passed to the inner's decision-making module
        and returns a diagnostic index. The returned diagnostic index must be
        passed to the `utils.encoding.diagnosis_indexes` dictionary as a key
        in order to obtain the diagnostis' title.

        Returns
        -------
        :return: A diagnosis index
        """
        diagnosis = self.engine.predict([
            [
                self.fact.sex,
                self.fact.age,
                self.fact.height,
                self.fact.weight,
                self.fact.HR,
                self.fact.Pd,
                self.fact.PQ,
                self.fact.QRS,
                self.fact.QT,
                self.fact.QTcFra
            ]
        ])

        return diagnosis[0]
