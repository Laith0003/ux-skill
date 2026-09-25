import { useForm } from "react-hook-form";

type Values = { displayName: string; email: string; timezone: string };

export function SettingsForm({ defaults, timezones }: { defaults: Values; timezones: string[] }) {
  const { register, handleSubmit, formState } = useForm<Values>({ defaultValues: defaults });

  return (
    <form className="settings-form grid gap-6" onSubmit={handleSubmit(save)} noValidate>
      <fieldset className="grid gap-4">
        <legend className="text-base font-semibold">Profile</legend>

        <div className="field">
          <label htmlFor="displayName">Display name</label>
          <input
            id="displayName"
            type="text"
            autoComplete="nickname"
            placeholder="How teammates see you"
            aria-describedby="displayName-hint"
            {...register("displayName", { required: true })}
          />
          <p id="displayName-hint" className="field-hint">
            Shown on comments and assignments.
          </p>
        </div>

        <div className="field">
          <label htmlFor="email">Work email</label>
          <input
            id="email"
            type="email"
            autoComplete="email"
            placeholder="name@company.com"
            aria-invalid={formState.errors.email ? "true" : "false"}
            aria-describedby="email-error"
            {...register("email", { required: "Enter the email you sign in with" })}
          />
          {formState.errors.email ? (
            <p id="email-error" role="alert" className="field-error">
              {formState.errors.email.message}
            </p>
          ) : null}
        </div>

        <div className="field">
          <label htmlFor="timezone">Time zone</label>
          <select id="timezone" {...register("timezone")}>
            {timezones.map((tz) => (
              <option key={tz} value={tz}>
                {tz}
              </option>
            ))}
          </select>
        </div>
      </fieldset>

      <div className="flex justify-end gap-3">
        <button type="reset" className="btn btn-quiet">
          Discard changes
        </button>
        <button type="submit" className="btn btn-primary" disabled={formState.isSubmitting}>
          Save profile
        </button>
      </div>
    </form>
  );
}

async function save(values: Values) {
  await fetch("/api/settings", { method: "PUT", body: JSON.stringify(values) });
}
