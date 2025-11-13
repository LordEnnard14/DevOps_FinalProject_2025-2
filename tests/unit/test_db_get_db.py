import pytest

from app import db as dbmod


def test_get_db_yields_and_closes(db_session, monkeypatch):
    # Hacemos que get_db use la misma session de la fixture para poder ejecutar el finally
    monkeypatch.setattr(dbmod, "SessionLocal", lambda: db_session)
    gen = dbmod.get_db()
    s = next(gen)
    assert s is db_session
    # cerrar el generador -> ejecuta el finally y cierra la sesión
    with pytest.raises(StopIteration):
        next(gen)
