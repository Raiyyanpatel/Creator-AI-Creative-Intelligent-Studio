import React from 'react';

interface ChipProps {
  label: string;
  variant?: 'default' | 'ai' | 'accent' | 'success';
  icon?: React.ReactNode;
  onClick?: () => void;
  selected?: boolean;
}

export const Chip: React.FC<ChipProps> = ({
  label,
  variant = 'default',
  icon,
  onClick,
  selected = false,
}) => {
  const getStyles = (): React.CSSProperties => {
    let bg = 'var(--bg-surface-3)';
    let color = 'var(--text-secondary)';
    let border = '1px solid rgba(255, 255, 255, 0.06)';

    if (variant === 'ai' || selected) {
      bg = 'var(--ai-soft)';
      color = 'var(--ai-accent)';
      border = '1px solid var(--ai-border)';
    } else if (variant === 'success') {
      bg = 'rgba(167, 243, 107, 0.15)';
      color = 'var(--success)';
      border = '1px solid rgba(167, 243, 107, 0.3)';
    }

    return {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '5px',
      padding: '5px 10px',
      borderRadius: 'var(--radius-pill)',
      fontSize: '11px',
      fontWeight: 500,
      backgroundColor: bg,
      color,
      border,
      cursor: onClick ? 'pointer' : 'default',
      userSelect: 'none',
      margin: '3px 4px 3px 0',
      transition: 'all 0.15s ease',
    };
  };

  return (
    <span style={getStyles()} onClick={onClick}>
      {icon}
      {label}
    </span>
  );
};
