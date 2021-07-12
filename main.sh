pip -q --disable-pip-version-check install repl-cli
pip -q --disable-pip-version-check install python3-protobuf
pip -q --disable-pip-version-check uninstall -y protobuf python3-protobuf
pip -q --disable-pip-version-check install --upgrade protobuf
replit login $SID
python main.py