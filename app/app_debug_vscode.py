import debugpy
import streamlit as st
import app

# pylint: disable=invalid-name
markdown = st.markdown(
"""
## Ready to attach the VS Code Debugger!
![Python: Remote Attach](https://awesome-streamlit.readthedocs.io/en/latest/_images/vscode_python_remote_attach.png)
for more info see the [VS Code section at awesome-streamlit.readthedocs.io]
(https://awesome-streamlit.readthedocs.io/en/latest/vscode.html#integrated-debugging)
"""
)

if not debugpy.is_client_connected():
    debugpy.listen(5679)
    debugpy.wait_for_client()

markdown.empty()

app.main()