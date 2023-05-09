import { Switch } from "antd";

const RequiredWidget = ({
  value,
  onChange,
  path,
  fullSchema,
  updateRequired,
}) => {
  const handleChange = checked => {
    // onChange(checked);
    addRequiredToParent(path.get("path").toJS(), checked);
    // onChange(checked);
  };

  const addRequiredToParent = (schemaPath, checked) => {
    if (schemaPath.length) {
      const parentPath = findParentPath(schemaPath);
      const fieldName = schemaPath[schemaPath.length - 1];
      updateRequired(parentPath, fieldName, checked);
      addRequiredToParent(parentPath, checked);
    }
  };

  const updateRequiredxx = (path, fieldName, isRequired) => {
    let schema = fullSchema.getIn([...path]).toJS();

    let required = schema.required || [];

    if (isRequired) {
      if (!required.includes(fieldName)) {
        required.push(fieldName);
      }
    } else {
      required = required.filter(e => e !== fieldName);
    }

    // TODO: If required is gonna be empty, just remove the property altogether
    // TODO: If we remove an element from the tree, we should remove it from the required as well
    // Objects have to be required always for validation to work inside

    let updatedSchema = { ...schema, required };

    return updatedSchema;
  };

  const findParentPath = schemaPath => {
    let isObj;
    for (let i = schemaPath.length - 1; i >= 0; i--) {
      // If we find a properties, it means we're inside an object (and not an array)
      if (schemaPath[i] === "properties") {
        isObj = true;
      } else if (isObj) {
        return schemaPath.splice(0, i + 1);
      } else {
        isObj = false;
      }
    }
    return [];
  };

  return (
    <Switch onChange={handleChange} checked={value}>
      Required
    </Switch>
  );
};

export default RequiredWidget;
