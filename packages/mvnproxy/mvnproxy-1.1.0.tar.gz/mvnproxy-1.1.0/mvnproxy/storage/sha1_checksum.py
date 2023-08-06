import hashlib

from mvnproxy.storage import cache_path


def compute_sha1_checksum(path: str) -> None:
    # we remove the .sha1 suffix
    file_path = cache_path(path)
    with open(file_path[:-5], "rb") as input_file:
        with open(file_path, "wt") as output_file:
            sha_1 = hashlib.sha1()
            sha_1.update(input_file.read())
            output_file.write(sha_1.hexdigest())
            output_file.write("\n")
