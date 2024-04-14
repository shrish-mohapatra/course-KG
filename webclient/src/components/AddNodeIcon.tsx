interface AddNodeIconProps {
  color?: string;
}

const AddNodeIcon = ({ color = "#6B6B6B" }: AddNodeIconProps) => {
  return (
    <svg
      width="24"
      height="27"
      viewBox="0 0 24 27"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <svg
        width="24"
        height="27"
        viewBox="0 0 24 27"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle
          cx="18.0625"
          cy="13.5"
          r="5.0625"
          transform="rotate(90 18.0625 13.5)"
          fill={color}
        />
        <circle
          cx="5.40625"
          cy="21.9375"
          r="5.0625"
          transform="rotate(90 5.40625 21.9375)"
          fill={color}
        />
        <circle
          cx="5.40625"
          cy="5.0625"
          r="5.0625"
          transform="rotate(90 5.40625 5.0625)"
          fill={color}
        />
      </svg>
    </svg>
  );
};

export default AddNodeIcon;
