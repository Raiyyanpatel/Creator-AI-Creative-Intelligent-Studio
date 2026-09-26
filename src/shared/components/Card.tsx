import React from 'react';

interface CardProps {
  children: React.ReactNode;
  variant?: 'surface' | 'elevated' | 'glass' | 'ai';
  padding?: string | number;
  borderRadius?: string;
  onClick?: () => void;
  style?: React.CSSProperties;
  className?: string;
}

export const Card: React.FC<CardProps> = ({
  children,
  variant = 'surface',
  padding = '18px',
  borderRadius = 'var(--radius-lg)',
  onClick,
  style = {},
  className = '',
}) => {
  const getStyles = (): React.CSSProperties => {
    let bg = 'var(--bg-surface)';
    let border = '1px solid rgba(255, 255, 255, 0.07)';

    if (variant === 'elevated') {
      bg = 'var(--bg-surface-2)';
      border = '1px solid rgba(255, 255, 255, 0.09)';
    } else if (variant === 'glass') {
      bg = 'rgba(23, 23, 23, 0.7)';
      border = '1px solid rgba(255, 255, 255, 0.1)';
    } else if (variant === 'ai') {
      bg = 'linear-gradient(145deg, #161c0c, #111111)';
      border = '1px solid var(--ai-border)';
    }

    return {
      backgroundColor: bg,
      borderRadius,
      padding,
      border,
      position: 'relative',
      cursor: onClick ? 'pointer' : 'default',
      transition: 'transform 0.18s ease, border-color 0.18s ease',
      ...style,
    };
  };

  return (
    <div style={getStyles()} onClick={onClick} className={className}>
      {children}
    </div>
  );
};
