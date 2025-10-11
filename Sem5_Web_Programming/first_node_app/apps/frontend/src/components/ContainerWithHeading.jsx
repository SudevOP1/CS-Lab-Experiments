const ContainerWithHeading = ({
  children,
  heading,
  innerDivClassNames,
  headingClassNames,
}) => {
  return (
    <div>
      <p
        className={`text-2xl font-bold translate-x-5 translate-y-2/5 px-2 bg-white w-fit ${headingClassNames}`}
      >
        {heading}
      </p>
      <div className={`px-6 py-6 border border-1-black ${innerDivClassNames}`}>
        {children}
      </div>
    </div>
  );
};

export default ContainerWithHeading;
