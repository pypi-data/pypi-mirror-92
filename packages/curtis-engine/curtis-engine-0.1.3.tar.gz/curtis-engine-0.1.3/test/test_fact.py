from curtis.fact import CurtisFact
from curtis.exceptions import CurtisParameterError
from curtis.utils.validation import validation_bounds


def test_creates_fact_instance():
    """ Should correctly create a `CurtisFact` instance. """
    fact = CurtisFact(
        sex=1,
        age=89,
        height=140,
        weight=30,
        HR=56,
        Pd=122,
        PQ=164,
        QRS=118,
        QT=460,
        QTcFra=451
    )

    assert isinstance(fact, CurtisFact)

    assert fact.sex == 1
    assert fact.age == 89
    assert fact.height == 140
    assert fact.weight == 30
    assert fact.HR == 56
    assert fact.Pd == 122
    assert fact.PQ == 164
    assert fact.QRS == 118
    assert fact.QT == 460
    assert fact.QTcFra == 451


def test_excepts_invalid_fact():
    """ Should not create a `CurtisFact` instance and raise an exception. """
    try:
        CurtisFact()
    except:
        assert True


def test_excepts_invalid_sex():
    """ Should not create a `CurtisFact` instance and raise an exception. """
    try:
        CurtisFact(
            sex=2,  # <- Cause
            age=89,
            height=140,
            weight=30,
            HR=56,
            Pd=122,
            PQ=164,
            QRS=118,
            QT=460,
            QTcFra=451
        )
    except CurtisParameterError as e:
        assert str(e) == validation_bounds['sex']['reason']


def test_excepts_invalid_age():
    """ Should not create a `CurtisFact` instance and raise an exception. """
    try:
        CurtisFact(
            sex=1,
            age=0,  # <- Cause
            height=140,
            weight=30,
            HR=56,
            Pd=122,
            PQ=164,
            QRS=118,
            QT=460,
            QTcFra=451
        )
    except CurtisParameterError as e:
        assert str(e) == validation_bounds['age']['reason']


def test_excepts_invalid_height():
    """ Should not create a `CurtisFact` instance and raise an exception. """
    try:
        CurtisFact(
            sex=1,
            age=0,
            height=450,  # <- Cause
            weight=30,
            HR=56,
            Pd=122,
            PQ=164,
            QRS=118,
            QT=460,
            QTcFra=451
        )
    except CurtisParameterError as e:
        assert str(e) == validation_bounds['height']['reason']


def test_excepts_invalid_weight():
    """ Should not create a `CurtisFact` instance and raise an exception. """
    try:
        CurtisFact(
            sex=1,
            age=0,
            height=140,
            weight=501,  # <- Cause
            HR=56,
            Pd=122,
            PQ=164,
            QRS=118,
            QT=460,
            QTcFra=451
        )
    except CurtisParameterError as e:
        assert str(e) == validation_bounds['weight']['reason']


def test_excepts_invalid_HR():
    """ Should not create a `CurtisFact` instance and raise an exception. """
    try:
        CurtisFact(
            sex=1,
            age=0,
            height=140,
            weight=30,
            HR=120,  # <- Cause
            Pd=122,
            PQ=164,
            QRS=118,
            QT=460,
            QTcFra=451
        )
    except CurtisParameterError as e:
        assert str(e) == validation_bounds['HR']['reason']


def test_excepts_invalid_Pd():
    """ Should not create a `CurtisFact` instance and raise an exception. """
    try:
        CurtisFact(
            sex=1,
            age=0,
            height=140,
            weight=30,
            HR=56,
            Pd=69,  # <- Cause
            PQ=164,
            QRS=118,
            QT=460,
            QTcFra=451
        )
    except CurtisParameterError as e:
        assert str(e) == validation_bounds['Pd']['reason']


def test_excepts_invalid_PQ():
    """ Should not create a `CurtisFact` instance and raise an exception. """
    try:
        CurtisFact(
            sex=1,
            age=0,
            height=140,
            weight=30,
            HR=56,
            Pd=122,
            PQ=220,  # <- Cause
            QRS=118,
            QT=460,
            QTcFra=451
        )
    except CurtisParameterError as e:
        assert str(e) == validation_bounds['PQ']['reason']


def test_excepts_invalid_QRS():
    """ Should not create a `CurtisFact` instance and raise an exception. """
    try:
        CurtisFact(
            sex=1,
            age=0,
            height=140,
            weight=30,
            HR=56,
            Pd=122,
            PQ=164,
            QRS=180,  # <- Cause
            QT=460,
            QTcFra=451
        )
    except CurtisParameterError as e:
        assert str(e) == validation_bounds['QRS']['reason']


def test_excepts_invalid_QT():
    """ Should not create a `CurtisFact` instance and raise an exception. """
    try:
        CurtisFact(
            sex=1,
            age=0,
            height=140,
            weight=30,
            HR=56,
            Pd=122,
            PQ=164,
            QRS=118,
            QT=320,  # <- Cause
            QTcFra=451
        )
    except CurtisParameterError as e:
        assert str(e) == validation_bounds['QT']['reason']


def test_excepts_invalid_QTcFra():
    """ Should not create a `CurtisFact` instance and raise an exception. """
    try:
        CurtisFact(
            sex=1,
            age=0,
            height=140,
            weight=30,
            HR=56,
            Pd=122,
            PQ=164,
            QRS=118,
            QT=460,
            QTcFra=520  # <- Cause
        )
    except CurtisParameterError as e:
        assert str(e) == validation_bounds['QTcFra']['reason']
