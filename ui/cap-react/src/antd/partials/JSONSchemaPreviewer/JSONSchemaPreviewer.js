import { MosesForm } from "cap-moses";
import PropTypes from "prop-types";

const JSONSchemaPreviewer = ({
  isPublished,
  schema,
  uiSchema,
  children,
  display = "tabView",
  onChange,
  onSubmit,
  formData,
  className,
}) => {
  return (
    schema && (
      <MosesForm
        className={className}
        schema={schema}
        showErrorList={false}
        uiSchema={{
          "ui:readonly": true,
          ...uiSchema,
          "ui:object": display,
        }}
        liveValidate={false}
        noValidate={true}
        onError={() => {}}
        formData={formData}
        onBlur={() => {}}
        onChange={onChange}
        onSubmit={onSubmit}
        formContext={{
          tabView: display === "tabView",
          readonlyPreview: true,
          isPublished: isPublished,
        }}
      >
        {children}
      </MosesForm>
    )
  );
};

JSONSchemaPreviewer.propTypes = {
  display: PropTypes.string,
  children: PropTypes.node,
  isPublished: PropTypes.bool,
  schema: PropTypes.object,
  uiSchema: PropTypes.object,
  onChange: PropTypes.func,
  onSubmit: PropTypes.func,
};

export default JSONSchemaPreviewer;
