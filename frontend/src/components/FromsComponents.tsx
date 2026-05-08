import { CircleUserRound, Building2, ChartNoAxesCombined, Smile } from "lucide-react";

const icons = {
    profile: <CircleUserRound />,
    departement: <Building2 />,
    experience: <ChartNoAxesCombined />,
    satisfaction: <Smile />
}


export const Label = ({ children } : any) => (
  <label className="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">{children}</label>
);

export const Input = ({ ...props }) => (
  <input
    className="w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-transparent transition"
    {...props}
  />
);

export const Select = ({ children, ...props } : any) => (
  <select
    className="w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-transparent transition"
    {...props}
  >
    {children}
  </select>
);

export const RatingSelect = ({ max = 4, ...props }: any) => (
  <Select {...props}>
    {Array.from({ length: max }, (_, i) => (
      <option key={i + 1} value={i + 1}>{i + 1}</option>
    ))}
  </Select>
);

export const SectionTitle = ({ icon, title, color }: any) => (
  <div className={`flex items-center gap-2 mb-4 pb-2 border-b ${color}`}>
    {icons[icon]}
    <h3 className="text-sm font-semibold uppercase tracking-widest text-gray-600">{title}</h3>
  </div>
);



export const FormGrid = ({ children }: any) => {
  return <div className="grid grid-cols-2 gap-x-4 gap-y-4">{children}</div>;
}