import { cva } from "class-variance-authority";

// Variant class strings live here so components stay small. They are class
// lists, not copy; the linter reads them as classes.
export const button = cva(
  [
    "inline-flex items-center justify-center gap-2",
    "min-h-11 rounded-md px-4 text-sm font-medium",
    "transition-colors duration-150 ease-out",
    "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber-700",
    "disabled:cursor-not-allowed disabled:opacity-60",
  ],
  {
    variants: {
      intent: {
        primary: "bg-teal-700 text-white hover:bg-teal-800",
        secondary: "border border-stone-300 bg-white text-stone-900 hover:bg-stone-50",
        danger: "bg-red-700 text-white hover:bg-red-800",
      },
      size: {
        sm: "min-h-9 px-3 text-xs",
        md: "",
        lg: "min-h-12 px-5 text-base",
      },
    },
    defaultVariants: { intent: "primary", size: "md" },
  },
);

export const badge = {
  neutral: "rounded bg-stone-100 px-2 py-0.5 text-xs text-stone-700",
  warning: "rounded bg-amber-100 px-2 py-0.5 text-xs text-amber-900",
};
