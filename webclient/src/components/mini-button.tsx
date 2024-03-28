type MiniButtonProps = {
    title: string
}

const MiniButton = ({ title }: MiniButtonProps) => {
    return (
        <button className="border-neutral-600 bg-neutral-800 px-2 border rounded-full h-[22px] text-sm">
            <span>{title}</span>
        </button>
    )
}

export default MiniButton