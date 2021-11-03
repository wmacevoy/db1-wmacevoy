import googleform2isoformat

def test_googleform2isodatetime():
    formTime="11/2/2021 16:16:14"
    dbTime="2021-11-02T16:16:14"

    result=googleform2isoformat.googleform2isoformat(formTime)

    if (dbTime != result):
        raise ValueError(result)
