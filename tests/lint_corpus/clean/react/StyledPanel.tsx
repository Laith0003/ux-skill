import styled, { css } from "styled-components";

const focusRing = css`
  &:focus-visible {
    outline: 2px solid var(--focus);
    outline-offset: 2px;
  }
`;

export const Panel = styled.section<{ $elevated?: boolean }>`
  display: grid;
  gap: var(--space-4);
  padding-block: var(--space-6);
  padding-inline: var(--space-5);
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: var(--surface);
  ${({ $elevated }) =>
    $elevated &&
    css`
      box-shadow: 0 1px 2px rgb(15 23 42 / 0.06);
    `}
`;

export const PanelAction = styled.button`
  justify-self: start;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-sm);
  background: var(--action);
  color: var(--on-action);
  transition: background-color 150ms ease-out, transform 150ms ease-out;
  ${focusRing}

  &:active {
    transform: translateY(1px);
  }

  @media (prefers-reduced-motion: reduce) {
    transition: none;
  }
`;
