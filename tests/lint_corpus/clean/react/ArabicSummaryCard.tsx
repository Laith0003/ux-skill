type Summary = { orders: number; revenue: string; refunds: number };

// Arabic dashboard card. Uses logical utilities (ms-, pe-, text-start) so the
// layout mirrors under dir="rtl" without a second stylesheet.
export function ArabicSummaryCard({ summary }: { summary: Summary }) {
  return (
    <section dir="rtl" lang="ar" className="summary-card rounded-lg border border-line p-6 text-start">
      <h2 className="text-xl font-semibold">ملخص الأسبوع</h2>
      <p className="mt-2 text-ink-muted">آخر تحديث قبل ٥ دقائق من سجل الطلبات.</p>
      <dl className="mt-6 grid grid-cols-2 gap-4">
        <div className="ps-4 border-s border-line">
          <dt className="text-sm text-ink-muted">الطلبات</dt>
          <dd className="text-2xl font-semibold tabular-nums">{summary.orders}</dd>
        </div>
        <div className="ps-4 border-s border-line">
          <dt className="text-sm text-ink-muted">الإيرادات</dt>
          <dd className="text-2xl font-semibold tabular-nums">{summary.revenue}</dd>
        </div>
        <div className="ps-4 border-s border-line">
          <dt className="text-sm text-ink-muted">المرتجعات</dt>
          <dd className="text-2xl font-semibold tabular-nums">{summary.refunds}</dd>
        </div>
      </dl>
      <a className="mt-6 inline-flex items-center gap-2 me-auto" href="/ar/reports/weekly">
        عرض التقرير الأسبوعي كاملاً
      </a>
    </section>
  );
}
