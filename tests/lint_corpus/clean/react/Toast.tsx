import { cva, type VariantProps } from "class-variance-authority";

const toast = cva("toast flex items-start gap-3 rounded-md border px-4 py-3 text-sm", {
  variants: {
    tone: {
      info: "border-line bg-surface text-ink",
      success: "border-positive/40 bg-positive-subtle text-ink",
      error: "border-critical/50 bg-critical-subtle text-ink",
    },
  },
  defaultVariants: { tone: "info" },
});

type ToastProps = VariantProps<typeof toast> & {
  message: string;
  actionLabel?: string;
  onAction?: () => void;
};

export function Toast({ tone, message, actionLabel, onAction }: ToastProps) {
  // Errors interrupt: role="alert" is assertive. Info and success wait politely.
  const isError = tone === "error";

  return (
    <div
      className={toast({ tone })}
      role={isError ? "alert" : "status"}
      aria-live={isError ? "assertive" : "polite"}
    >
      <p className="flex-1">{message}</p>
      {actionLabel && onAction ? (
        <button type="button" className="text-link font-medium" onClick={onAction}>
          {actionLabel}
        </button>
      ) : null}
    </div>
  );
}
