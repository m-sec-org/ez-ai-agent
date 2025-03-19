import { IconProps } from "@/types/props";

export function ChromeIcon({
  width = 12,
  height = 12,
  color = "currentColor",
}: IconProps) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width={width}
      height={height}
      viewBox="0 0 12 12"
      fill="none"
    >
      <g clipPath="url(#clip0_2850_3925)">
        <path
          d="M6.66675 11C9.42817 11 11.6667 8.76142 11.6667 6C11.6667 3.23858 9.42817 1 6.66675 1C3.90532 1 1.66675 3.23858 1.66675 6C1.66675 8.76142 3.90532 11 6.66675 11Z"
          stroke={color}
          strokeWidth="1.25"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M6.66675 8C7.77132 8 8.66675 7.10457 8.66675 6C8.66675 4.89543 7.77132 4 6.66675 4C5.56218 4 4.66675 4.89543 4.66675 6C4.66675 7.10457 5.56218 8 6.66675 8Z"
          stroke={color}
          strokeWidth="1.25"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M11.2517 4H6.66675"
          stroke={color}
          strokeWidth="1.25"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M2.64172 3.03003L4.93672 7.00003"
          stroke={color}
          strokeWidth="1.25"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M6.10669 10.97L8.39669 7"
          stroke={color}
          strokeWidth="1.25"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </g>
      <defs>
        <clipPath id="clip0_2850_3925">
          <rect
            width={width}
            height={height}
            fill="white"
            transform="translate(0.666748)"
          />
        </clipPath>
      </defs>
    </svg>
  );
}
