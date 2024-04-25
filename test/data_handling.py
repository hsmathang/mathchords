from mathchords.io import ExperimentHandler

# Const data
TEST_DATA = {"foo": True}

# Handler instantiation
handler = ExperimentHandler("data/test/")

# Handler write/read test
handler.write(TEST_DATA, "test.pkl")
digestion = handler.read("test.pkl")
print(digestion)