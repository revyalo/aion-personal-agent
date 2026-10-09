import aion.database


def test_database_path_is_stable(tmp_path, monkeypatch):
    original_path = aion.database.DATABASE_PATH

    # La ruta debe ser absoluta.
    assert original_path.is_absolute()

    # Simulamos ejecutar Python desde otra carpeta.
    monkeypatch.chdir(tmp_path)

    # La ubicación de la DB no debe cambiar.
    assert aion.database.DATABASE_PATH == original_path
    assert original_path.parent.name == "data"
