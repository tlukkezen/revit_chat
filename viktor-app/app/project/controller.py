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

import pickle

from viktor import UserError
from viktor import ViktorController
from viktor.core import Storage
from viktor.core import File
from viktor.views import WebResult
from viktor.views import WebView
from tempfile import NamedTemporaryFile
import ifcopenshell
from ifcopenshell.util import element as Element
import json
from app.project.parametrization import Parametrization

from ..AI_search.chat_view import generate_html_code
from ..AI_search.retrieval_assistant import RetrievalAssistant
from pathlib import Path
from viktor.views import IFCView, IFCResult


def get_object_data_by_classes(file, class_type):
    objects_data = []
    objects = file.by_type(class_type)
    for obj in objects:
        obj_id = obj.id()
        objects_data.append({
            'ExpressID': obj.id(),
            'GlobalId': obj.GlobalId,
            'Class': obj.is_a(),
            'PredefinedType': Element.get_predefined_type(obj),
            'Name': obj.Name,
            'Level': Element.get_container(obj).Name
            if Element.get_container(obj)
            else '',
            'ObjectType': Element.get_type(obj).Name
            if Element.get_type(obj)
            else '',
            'QuantitySets': Element.get_psets(obj, qtos_only=True),
            'PropertySets': Element.get_psets(obj, psets_only=True),
        })
    return objects_data

class Controller(ViktorController):
    """Controller class for Document searcher app"""

    label = "Documents"
    parametrization = Parametrization

    def push_model(self, params, **kwargs):
        """Function to push the uploaded IFC file to the Storage"""
        if not params.input.ifcfile:
            raise UserError("Please upload an IFC file first.")

        temp_f = NamedTemporaryFile(suffix=".ifc", delete=False, mode="w")
        temp_f.write(params.input.ifcfile.file.getvalue())
        model = ifcopenshell.open(Path(temp_f.name))
        data = get_object_data_by_classes(model, "IfcBuildingElement")
        json.dumps(data)

    @WebView("Conversation", duration_guess=5)
    def conversation(self, params, **kwargs):
        """View for showing the questions, answers and sources to the user."""
        if not params.input.embeddings_are_set:
            raise UserError("Please embed the uploaded PDF file first, by clicking 'Submit document(s)'.")
        df = pickle.loads(Storage().get("embeddings_storage", scope="entity").getvalue_binary())
        retrieval_assistant = RetrievalAssistant(params.input.question, df)
        answer = retrieval_assistant.ask_assistant()
        html = generate_html_code(
            params.input.question, answer, retrieval_assistant.metadata_list, retrieval_assistant.context_list
        )
        return WebResult(html=html)

    @IFCView("IFC view", duration_guess=1)
    def get_ifc_view(self, params, **kwargs):
        return IFCResult(params.input.ifcfile)
