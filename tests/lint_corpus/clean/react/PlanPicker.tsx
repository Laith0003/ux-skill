import { cn } from "../lib/cn";
import { formatMoney } from "../lib/money";

type Plan = {
  id: string;
  name: string;
  monthly: number;
  seats: string;
  features: string[];
};

export function PlanPicker({ plans, selected, onPick }: { plans: Plan[]; selected: string; onPick: (id: string) => void }) {
  return (
    <fieldset className="plan-picker">
      <legend className="text-lg font-semibold">Choose a plan</legend>
      <div className="mt-4 grid gap-4 md:grid-cols-[1.2fr_1fr]">
        {plans.map((plan) => {
          const isSelected = plan.id === selected;
          return (
            <label
              key={plan.id}
              className={cn(
                "plan-option relative flex flex-col gap-3 rounded-md border p-5",
                isSelected ? "border-ink ring-1 ring-ink" : "border-line",
              )}
            >
              <input
                type="radio"
                name="plan"
                value={plan.id}
                checked={isSelected}
                onChange={() => onPick(plan.id)}
                className="sr-only"
              />
              <span className="font-medium">{plan.name}</span>
              <span className="text-2xl tabular-nums">
                {formatMoney(plan.monthly)} <span className="text-sm text-ink-muted">per month</span>
              </span>
              <span className="text-sm text-ink-muted">{plan.seats}</span>
              <ul className="mt-2 list-disc ps-5 text-sm">
                {plan.features.map((feature) => (
                  <li key={feature}>{feature}</li>
                ))}
              </ul>
            </label>
          );
        })}
      </div>
    </fieldset>
  );
}
