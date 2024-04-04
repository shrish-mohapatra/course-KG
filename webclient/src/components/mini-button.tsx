type MiniButtonProps = {
    title: string
    onClick: React.MouseEventHandler<HTMLButtonElement> | undefined
}

const MiniButton = ({ title, onClick }: MiniButtonProps) => {
    return (
        <button onClick={onClick} className="border-neutral-600 bg-neutral-800 px-2 border rounded-full h-[22px] text-xs text-zinc-300">
            <span>{title}</span>
        </button>
    )
}

export default MiniButton