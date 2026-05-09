def test_generate_short_code_mock(mocker):
    from src.todo import utils
    mocker.patch("random.choices", return_value=list("qwerty12345"))
    code = utils.generate_short_code()
    assert code == "qwerty12345"