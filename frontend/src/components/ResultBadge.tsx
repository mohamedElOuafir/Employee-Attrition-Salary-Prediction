


export const ResultBadge = ({ result, type }: any) => {
  if (!result) return null;
  const isAttrition = type === "attrition";
  const isYes = result?.prediction_label === "Yes";
  const color = isAttrition
    ? (isYes ? "bg-red-50 border-red-200 text-red-700" : "bg-emerald-50 border-emerald-200 text-emerald-700")
    : "bg-indigo-50 border-indigo-200 text-indigo-700";
  return (
    <div className={`mt-6 p-4 rounded-xl border ${color} flex items-center gap-3`}>
      <div className="text-2xl">{isAttrition ? (isYes ? "⚠️" : "✅") : "💰"}</div>
      <div>
        <p className="text-xs uppercase tracking-wide font-semibold opacity-70">Résultat de la prédiction</p>
        <p className="text-base font-bold mt-0.5">
          {isAttrition
            ? (isYes ? "Risque d'attrition élevé" : "Employé stable")
            : `Salaire estimé : ${Number(result.predicted_salary.toFixed(2)).toLocaleString("fr-FR")} MAD`}
        </p>
        
      </div>
    </div>
  );
};