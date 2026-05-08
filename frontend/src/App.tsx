import { useState } from "react";
import { AttritionForm } from "./components/AttritionFrom";
import { SalaryForm } from "./components/SalaryForm";
import { TriangleAlert , CircleDollarSign} from "lucide-react";





export default function App() {
  const [tab, setTab] = useState("attrition");

  return (
    <div className="min-h-screen bg-gray-300 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        <div className="mb-6 text-center">
          <h1 className="text-2xl font-bold text-gray-800">HR Analytics — Prédictions RH</h1>
          <p className="text-sm text-gray-400 mt-1">Alimentez votre modèle ML avec les données employé</p>
        </div>

        <div className="flex bg-white border border-gray-100 rounded-xl p-1 mb-6 shadow-sm">
          <button
            onClick={() => setTab("attrition")}
            className={`flex items-center justify-center gap-2 flex-1 text-sm font-semibold py-2 rounded-lg transition ${tab === "attrition" ? "bg-red-500 text-white shadow-sm" : "text-gray-500 hover:text-gray-700"}`}
          >
            <TriangleAlert/>
            <span>Attrition</span>
          </button>
          <button
            onClick={() => setTab("salary")}
            className={`flex items-center justify-center gap-2 flex-1 text-sm font-semibold py-2 rounded-lg transition ${tab === "salary" ? "bg-indigo-500 text-white shadow-sm" : "text-gray-500 hover:text-gray-700"}`}
          >
            <CircleDollarSign />
            <span>Salaire</span>
          
          </button>
        </div>

        {tab === "attrition" ? <AttritionForm /> : <SalaryForm />}

        <p className="text-center text-xs text-gray-300 mt-4">
          Les boutons 📋 JSON copient le payload prêt à envoyer à votre API
        </p>
      </div>
    </div>
  );
}