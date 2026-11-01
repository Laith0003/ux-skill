import { badge } from "./button-variants";

type Invoice = { id: string; customer: string; amount: string; dueIn: number; overdue: boolean };

export function InvoiceCard({ invoice }: { invoice: Invoice }) {
  const tone = invoice.overdue ? badge.warning : badge.neutral;

  return (
    <article
      className={`group relative flex flex-col gap-3 rounded-lg border border-stone-200 bg-white p-5 ${
        invoice.overdue ? "border-amber-300" : ""
      }`}
    >
      <header className="flex items-baseline justify-between gap-4">
        <h3 className="truncate text-base font-semibold text-stone-900">{invoice.customer}</h3>
        <span className={tone}>{invoice.overdue ? "Overdue" : `Due in ${invoice.dueIn} days`}</span>
      </header>
      <p className="text-2xl tabular-nums text-stone-900">{invoice.amount}</p>
      <a
        href={`/invoices/${invoice.id}`}
        className="text-sm font-medium text-teal-800 underline-offset-4 hover:underline focus-visible:underline"
      >
        Open invoice {invoice.id}
      </a>
    </article>
  );
}
