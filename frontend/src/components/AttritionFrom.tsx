import { useState } from "react";
import { Label, SectionTitle, FormGrid, Input, Select, RatingSelect } from "./FromsComponents";
import { ResultBadge } from "./ResultBadge";
import {SearchCheck } from "lucide-react"; 
import type { AttritionEmployee } from "../models/interaces";


const DEPARTMENTS = ["Research & Development", "Sales", "Human Resources"];
const EDUCATION_FIELDS = ["Life Sciences", "Medical", "Marketing", "Technical Degree", "Human Resources", "Other"];
const JOB_ROLES = ["Sales Executive", "Research Scientist", "Laboratory Technician", "Manufacturing Director", "Healthcare Representative", "Manager", "Sales Representative", "Research Director", "Human Resources"];
const BUSINESS_TRAVEL = ["Non-Travel", "Travel_Rarely", "Travel_Frequently"];
const MARITAL_STATUS = ["Single", "Married", "Divorced"];

const defaultValues = {
  Age: 37, BusinessTravel: "Travel_Rarely", Department: "Research & Development",
  DistanceFromHome: 2, Education: 2, EducationField: "Other",
  EnvironmentSatisfaction: 4, Gender: "Male", JobInvolvement: 2,
  JobLevel: 1, JobRole: "Laboratory Technician", JobSatisfaction: 3,
  MaritalStatus: "Single", NumCompaniesWorked: 6, OverTime: "Yes",
  PercentSalaryHike: 15, RelationshipSatisfaction: 2, StockOptionLevel: 0,
  TotalWorkingYears: 7, TrainingTimesLastYear: 3, WorkLifeBalance: 3,
  YearsAtCompany: 0, YearsInCurrentRole: 0, YearsSinceLastPromotion: 0,
  YearsWithCurrManager: 0, MonthlyIncome: 2090,
};


export const AttritionForm = () => {

    const [form, setForm] = useState({ ...defaultValues });
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const set = (k: any) => (e: any) => setForm((f) => ({ ...f, [k]: isNaN(e.target.value) ? e.target.value : Number(e.target.value) || e.target.value }));



    const handleSubmit = async () => {
        setLoading(true);
        setResult(null);
        

        const attritionEmployee: AttritionEmployee = {
            Age: form.Age,
            BusinessTravel: form.BusinessTravel,
            Department: form.Department,
            DistanceFromHome: form.DistanceFromHome,
            Education: form.Education,
            EducationField: form.EducationField,
            EnvironmentSatisfaction: form.EnvironmentSatisfaction,
            Gender: form.Gender,
            JobInvolvement: form.JobInvolvement,
            JobLevel: form.JobLevel,
            JobRole: form.JobRole,
            JobSatisfaction: form.JobSatisfaction,
            MaritalStatus: form.MaritalStatus,
            MonthlyIncome: form.MonthlyIncome,
            NumCompaniesWorked: form.NumCompaniesWorked,
            OverTime: form.OverTime,
            PercentSalaryHike: form.PercentSalaryHike,
            RelationshipSatisfaction: form.RelationshipSatisfaction,
            StockOptionLevel: form.StockOptionLevel,
            TotalWorkingYears: form.TotalWorkingYears,
            TrainingTimesLastYear: form.TrainingTimesLastYear,
            WorkLifeBalance: form.WorkLifeBalance,
            YearsAtCompany: form.YearsAtCompany,
            YearsInCurrentRole: form.YearsInCurrentRole,
            YearsSinceLastPromotion: form.YearsSinceLastPromotion,
            YearsWithCurrManager: form.YearsWithCurrManager
        }
        try {
            console.log(attritionEmployee)
            const res = await fetch("http://localhost:8000/attrition/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(attritionEmployee),
            });
            const data = await res.json();
            console.log(data)
            setResult(data);
        } catch {
            console.log("error fetching results")
        } finally {
            setLoading(false);
        }
    };

    

    return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex flex-col gap-5">
        <div className="flex items-center justify-between">
            <div>
                <h2 className="text-xl font-bold text-gray-800">Prédiction d'attrition</h2>
                <p className="text-sm text-gray-400 mt-0.5">Estimez la probabilité qu'un employé quitte l'entreprise</p>
            </div>
            <span className="rounded-full bg-red-50 border border-red-100 text-red-500 text-xs font-semibold px-3 py-1">
                Attrition
            </span>
        </div>

        <SectionTitle icon="profile" title="Profil personnel" color="border-gray-100" />
        <FormGrid>
            <div>
                <Label>Âge</Label>
                <Input type="number" min={18} max={65} value={form.Age} onChange={set("Age")} />
            </div>
            <div>
                <Label>Genre</Label>
                <Select value={form.Gender} onChange={set("Gender")}>
                    <option>Male</option><option>Female</option>
                </Select>
            </div>
            <div>
                <Label>Statut marital</Label>
                <Select value={form.MaritalStatus} onChange={set("MaritalStatus")}>
                    {MARITAL_STATUS.map(m => <option key={m}>{m}</option>)}
                </Select>
            </div>
            <div>
                <Label>Distance domicile (km)</Label>
                <Input type="number" min={1} max={100} value={form.DistanceFromHome} onChange={set("DistanceFromHome")} />
            </div>
            <div>
                <Label>Niveau d'éducation (1–5)</Label>
                <RatingSelect max={5} value={form.Education} onChange={set("Education")} />
            </div>
            <div>
                <Label>Domaine d'étude</Label>
                <Select value={form.EducationField} onChange={set("EducationField")}>
                    {EDUCATION_FIELDS.map(f => <option key={f}>{f}</option>)}
                </Select>
            </div>
            <div>
                <Label>Salaire</Label>
                <Input type="number" step={0.01} min={1} value={form.MonthlyIncome} onChange={set("MonthlyIncome")} />
            </div>
        </FormGrid>

        <SectionTitle icon="departement" title="Poste & département" color="border-gray-100" />
        <FormGrid>
            <div>
                <Label>Département</Label>
                <Select value={form.Department} onChange={set("Department")}>
                    {DEPARTMENTS.map(d => <option key={d}>{d}</option>)}
                </Select>
            </div>
            <div>
                <Label>Rôle</Label>
                <Select value={form.JobRole} onChange={set("JobRole")}>
                    {JOB_ROLES.map(r => <option key={r}>{r}</option>)}
                </Select>
            </div>
            <div>
                <Label>Niveau de poste (1–5)</Label>
                <RatingSelect max={5} value={form.JobLevel} onChange={set("JobLevel")} />
            </div>
            <div>
                <Label>Heures supplémentaires</Label>
                <Select value={form.OverTime} onChange={set("OverTime")}>
                    <option>Yes</option>
                    <option>No</option>
                </Select>
            </div>
            <div>
                <Label>Déplacements prof.</Label>
                <Select value={form.BusinessTravel} onChange={set("BusinessTravel")}>
                    {BUSINESS_TRAVEL.map(b => <option key={b}>{b}</option>)}
                </Select>
            </div>
            <div>
                <Label>Stock options (0–3)</Label>
                <RatingSelect max={4} value={form.StockOptionLevel + 1} onChange={(e: any) => setForm(f => ({ ...f, StockOptionLevel: Number(e.target.value) - 1 }))}>
                {[0,1,2,3].map(v => <option key={v} value={v+1}>{v}</option>)}
                </RatingSelect>
            </div>
        </FormGrid>

        <SectionTitle icon="experience" title="Expérience & ancienneté" color="border-gray-100" />
        <FormGrid>
            <div>
                <Label>Années d'exp. totales</Label>
                <Input type="number" min={0} max={40} value={form.TotalWorkingYears} onChange={set("TotalWorkingYears")} />
            </div>
            <div>
                <Label>Nb entreprises antérieures</Label>
                <Input type="number" min={0} max={15} value={form.NumCompaniesWorked} onChange={set("NumCompaniesWorked")} />
            </div>
            <div>
                <Label>Années dans l'entreprise</Label>
                <Input type="number" min={0} max={40} value={form.YearsAtCompany} onChange={set("YearsAtCompany")} />
            </div>
            <div>
                <Label>Années au poste actuel</Label>
                <Input type="number" min={0} max={20} value={form.YearsInCurrentRole} onChange={set("YearsInCurrentRole")} />
            </div>
            <div>
                <Label>Années depuis promotion</Label>
                <Input type="number" min={0} max={20} value={form.YearsSinceLastPromotion} onChange={set("YearsSinceLastPromotion")} />
            </div>
            <div>
                <Label>Années avec manager</Label>
                <Input type="number" min={0} max={20} value={form.YearsWithCurrManager} onChange={set("YearsWithCurrManager")} />
            </div>
            <div>
                <Label>% hausse salaire</Label>
                <Input type="number" min={0} max={50} value={form.PercentSalaryHike} onChange={set("PercentSalaryHike")} />
            </div>
            <div>
                <Label>Formations (dernière année)</Label>
                <Input type="number" min={0} max={10} value={form.TrainingTimesLastYear} onChange={set("TrainingTimesLastYear")} />
            </div>
        </FormGrid>

        <SectionTitle icon="satisfaction" title="Satisfaction & engagement" color="border-gray-100" />
        <FormGrid>
            <div>
                <Label>Satisfaction environnement</Label>
                <RatingSelect value={form.EnvironmentSatisfaction} onChange={set("EnvironmentSatisfaction")} />
            </div>
            <div>
                <Label>Implication au travail</Label>
                <RatingSelect value={form.JobInvolvement} onChange={set("JobInvolvement")} />
            </div>
            <div>
                <Label>Satisfaction au poste</Label>
                <RatingSelect value={form.JobSatisfaction} onChange={set("JobSatisfaction")} />
            </div>
            <div>
                <Label>Satisfaction relations</Label>
                <RatingSelect value={form.RelationshipSatisfaction} onChange={set("RelationshipSatisfaction")} />
            </div>
            <div>
                <Label>Équilibre vie pro/perso</Label>
                <RatingSelect value={form.WorkLifeBalance} onChange={set("WorkLifeBalance")} />
            </div>
        </FormGrid>

        <div className="flex gap-3 mt-2">
            <button
                onClick={handleSubmit}
                disabled={loading}
                className="flex-1 bg-red-500 hover:bg-red-600 disabled:opacity-50 text-white font-semibold text-sm py-2.5 rounded-xl transition"
            >
                {loading ? 
                    "Analyse en cours…" : 
                    <div className={`flex items-center justify-center gap-2`}>
                        <SearchCheck />
                        <span>Prédire l'attrition</span>
                    </div>
                }
            </button>
            
        </div>

        <ResultBadge result={result} type="attrition" />
    </div>
    );
}