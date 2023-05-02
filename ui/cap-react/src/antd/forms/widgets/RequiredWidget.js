import { Switch } from "antd";

const RequiredWidget = ({ value, onChange, path, updateRequired }) => {
  const handleChange = checked => {
    onChange(checked);
    addRequiredToParent(path.get("path").toJS(), checked);
  };

  const addRequiredToParent = (schemaPath, checked) => {
    if (schemaPath.length) {
      const parentPath = findParentPath(schemaPath);
      const fieldName = schemaPath[schemaPath.length - 1];
      updateRequired(parentPath, fieldName, checked);
      addRequiredToParent(parentPath, checked);
    }
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
