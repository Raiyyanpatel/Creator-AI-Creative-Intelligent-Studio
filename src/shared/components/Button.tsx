import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'glass' | 'icon' | 'ai';
  size?: 'sm' | 'md' | 'lg';
  fullWidth?: boolean;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  fullWidth = false,
  children,
  className = '',
  style = {},
  ...props
}) => {
  const getStyles = (): React.CSSProperties => {
    const base: React.CSSProperties = {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontWeight: 600,
      letterSpacing: '-0.01em',
      cursor: 'pointer',
      border: 'none',
      outline: 'none',
      width: fullWidth ? '100%' : 'auto',
      transition: 'all 0.18s ease',
      borderRadius: variant === 'icon' ? '50%' : '14px',
    };

    // Size
    if (variant === 'icon') {
      const dim = size === 'sm' ? '34px' : size === 'lg' ? '46px' : '40px';
      base.width = dim;
      base.height = dim;
      base.padding = 0;
    } else {
      if (size === 'sm') {
        base.padding = '8px 14px';
        base.fontSize = '12px';
      } else if (size === 'lg') {
        base.padding = '16px 24px';
        base.fontSize = '16px';
        base.borderRadius = '18px';
      } else {
        base.padding = '12px 18px';
        base.fontSize = '14px';
      }
    }

    // Variants
    if (variant === 'primary' || variant === 'ai') {
      base.backgroundColor = 'var(--ai-accent)';
      base.color = '#080808';
      base.fontWeight = 700;
    } else if (variant === 'secondary') {
      base.backgroundColor = 'var(--bg-surface-3)';
      base.color = 'var(--text-primary)';
      base.border = '1px solid rgba(255, 255, 255, 0.08)';
    } else if (variant === 'glass') {
      base.backgroundColor = 'rgba(255, 255, 255, 0.08)';
      base.color = 'var(--text-primary)';
      base.backdropFilter = 'blur(10px)';
      base.border = '1px solid rgba(255, 255, 255, 0.12)';
    } else if (variant === 'icon') {
      base.backgroundColor = 'var(--bg-surface-2)';
      base.color = 'var(--text-primary)';
      base.border = '1px solid rgba(255, 255, 255, 0.06)';
    }

    return { ...base, ...style };
  };

  return (
    <button style={getStyles()} className={className} {...props}>
      {children}
    </button>
  );
};
