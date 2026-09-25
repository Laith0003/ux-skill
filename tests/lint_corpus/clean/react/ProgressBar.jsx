import PropTypes from "prop-types";

export function ProgressBar({ value, max = 100, label }) {
  const pct = Math.round((value / max) * 100);

  return (
    <div className="progress">
      <div className="progress-label">
        <span id="upload-progress-label">{label}</span>
        <span aria-hidden="true">{pct}%</span>
      </div>
      <div
        className="progress-track"
        role="progressbar"
        aria-labelledby="upload-progress-label"
        aria-valuemin={0}
        aria-valuemax={max}
        aria-valuenow={value}
      >
        <div className="progress-fill" style={{ transform: `scaleX(${pct / 100})` }} />
      </div>
    </div>
  );
}

ProgressBar.propTypes = {
  value: PropTypes.number.isRequired,
  max: PropTypes.number,
  label: PropTypes.string.isRequired,
};
