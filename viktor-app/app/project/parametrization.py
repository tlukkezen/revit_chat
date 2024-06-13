"""Copyright (c) 2023 VIKTOR B.V.
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.
VIKTOR B.V. PROVIDES THIS SOFTWARE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from viktor.parametrization import BooleanField
from viktor.parametrization import ChildEntityManager
from viktor.parametrization import SetParamsButton
from viktor.parametrization import Tab
from viktor.parametrization import Text
from viktor.parametrization import TextAreaField
from viktor.parametrization import ViktorParametrization
from viktor.parametrization import FileField


class Parametrization(ViktorParametrization):
    """Parametrization class for document searcher"""

    input = Tab("Input")
    input.welcome_text = Text(
        "# IFC chatter  \n"
        "Welcome to the VIKTOR document searcher. "
        "With this app, you can easily find information in your IFC documents. Your question will be answered using "
        "the power of AI."
    )
    input.text_step_1 = Text("**Step 1**: Upload your .IFC documents")
    input.ifcfile = FileField("ifcfile", description="Upload your .IFC file here", flex=100)
    input.text_step_2 = Text("**Step 2**: Submit your documents by clicking on the button below")
    input.confirm_model_button = SetParamsButton("Confirm model", "push_model", flex=45, longpoll=True)
    input.question = TextAreaField(
        "**Step 3:** Ask your question here",
        flex=100,
        description="Any language is allowed, the app will answer in the same language as your question.",
    )
    input.step_4_text = Text("**Step 4:** Get your result by clicking 'Update' in the lower-right corner of this app.")
