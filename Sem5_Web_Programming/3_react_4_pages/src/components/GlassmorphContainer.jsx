const GlassmorphContainer = ({ children, classNames = "" }) => {
  return (
    <div
      className={`w-200 min-h-100 bg-white/15 border-2 border-white/80
      rounded-4xl overflow-x-auto px-10 py-8 backdrop-blur-[20px] ${classNames}`}
    >
      {children}
    </div>
  );
};

export default GlassmorphContainer;
