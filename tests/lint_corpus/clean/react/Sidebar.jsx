import { NavLink } from "react-router-dom";

const sections = [
  { to: "/routes", label: "Routes", count: 12 },
  { to: "/drivers", label: "Drivers", count: 38 },
  { to: "/exceptions", label: "Exceptions", count: 7 },
];

export function Sidebar({ width, collapsed }) {
  return (
    <aside
      className="sidebar"
      aria-label="Workspace"
      style={{ "--sidebar-width": `${width}px` }}
      data-collapsed={collapsed ? "true" : "false"}
    >
      <nav>
        <ul className="sidebar__list">
          {sections.map((section) => (
            <li key={section.to}>
              <NavLink
                to={section.to}
                className={({ isActive }) => (isActive ? "sidebar__link is-active" : "sidebar__link")}
              >
                <span className="sidebar__label">{section.label}</span>
                <span className="sidebar__count" aria-label={`${section.count} items`}>
                  {section.count}
                </span>
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}
