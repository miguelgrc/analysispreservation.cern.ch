import { useEffect, useState } from "react";

import { Radio, Space, Tabs, Typography } from "antd";

import PropTypes from "prop-types";

import { SIZE_OPTIONS } from "../utils";
import PropertyKeyEditorForm from "./PropKeyEditorForm";

const JUSTIFY_OPTIONS = ["start", "center", "end"];

const Customize = ({
  schema,
  uiSchema,
  onSchemaChange,
  onUiSchemaChange,
  path,
  _path,
  _uiPath,
  fullSchema,
}) => {
  const [justify, setJustify] = useState(() => "start");
  const [size, setSize] = useState("xlarge");

  useEffect(() => {
    if (uiSchema && Object.hasOwn(uiSchema.toJS(), "ui:options")) {
      setSize(uiSchema.toJS()["ui:options"].size);
      setJustify(uiSchema.toJS()["ui:options"].justify);
    }
  }, [uiSchema]);

  const _onSchemaChange = (data, extra = "patata") => {
    // console.log(data);
    // console.log(schema.toJS());
    // console.log(fullSchema.toJS());
    // console.log(extra);
    if (extra && extra.path && extra.fieldName && extra.isRequired) {
      updateRequired(extra.path, extra.fieldName, extra.isRequired);
    } else {
      onSchemaChange(path.get("path").toJS(), data.formData);
    }
  };

  const updateRequired = (path, fieldName, isRequired) => {
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

    console.log("PATATA");
    console.log(updatedSchema);
  };

  const _onUiSchemaChange = data => {
    onUiSchemaChange(path.get("uiPath").toJS(), data.formData);
  };

  const sizeChange = newSize => {
    uiSchema = uiSchema ? uiSchema.toJS() : {};

    let { "ui:options": uiOptions = {}, ...rest } = uiSchema;
    let { size, ...restUIOptions } = uiOptions;

    size = newSize;
    let _uiOptions = { size, ...restUIOptions };

    onUiSchemaChange(path.get("uiPath").toJS(), {
      ...rest,
      "ui:options": _uiOptions,
    });
  };

  const alignChange = newAlign => {
    uiSchema = uiSchema ? uiSchema.toJS() : {};

    let { "ui:options": uiOptions = {}, ...rest } = uiSchema;
    let { justify, ...restUIOptions } = uiOptions;

    justify = newAlign;
    let _uiOptions = { justify, ...restUIOptions };

    onUiSchemaChange(path.get("uiPath").toJS(), {
      ...rest,
      "ui:options": _uiOptions,
    });
  };

  return (
    <Tabs
      className="scrollableTabs"
      centered
      style={{ flex: 1 }}
      items={[
        {
          key: "1",
          label: "Schema Settings",
          children: (
            <PropertyKeyEditorForm
              schema={schema && schema.toJS()}
              uiSchema={uiSchema && uiSchema.toJS()}
              formData={schema && schema.toJS()}
              onChange={_onSchemaChange}
              optionsSchemaObject="optionsSchema"
              optionsUiSchemaObject="optionsSchemaUiSchema"
            />
          ),
        },
        {
          key: "2",
          label: "UI Schema Settings",
          children:
            _path.size != 0 ? (
              <PropertyKeyEditorForm
                schema={schema && schema.toJS()}
                uiSchema={uiSchema && uiSchema.toJS()}
                formData={uiSchema && uiSchema.toJS()}
                onChange={_onUiSchemaChange}
                optionsSchemaObject="optionsUiSchema"
                optionsUiSchemaObject="optionsUiSchemaUiSchema"
                key={_uiPath}
              />
            ) : (
              <Space
                direction="vertical"
                style={{ padding: "0 12px", width: "100%" }}
              >
                <Typography.Text>Size Options</Typography.Text>
                <Radio.Group
                  size="small"
                  onChange={e => sizeChange(e.target.value)}
                  value={size}
                  style={{ paddingBottom: "15px" }}
                >
                  {Object.keys(SIZE_OPTIONS).map(size => (
                    <Radio.Button key={size} value={size}>
                      {size}
                    </Radio.Button>
                  ))}
                </Radio.Group>
                <Typography.Text>Align Options</Typography.Text>
                <Radio.Group
                  size="small"
                  onChange={e => alignChange(e.target.value)}
                  value={justify}
                >
                  {JUSTIFY_OPTIONS.map(justify => (
                    <Radio.Button key={justify} value={justify}>
                      {justify}
                    </Radio.Button>
                  ))}
                </Radio.Group>
              </Space>
            ),
        },
      ]}
    />
  );
};

Customize.propTypes = {
  schema: PropTypes.object,
  uiSchema: PropTypes.object,
  onSchemaChange: PropTypes.func,
  onUiSchemaChange: PropTypes.func,
  path: PropTypes.object,
  _path: PropTypes.object,
};

export default Customize;
