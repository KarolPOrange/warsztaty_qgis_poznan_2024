<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="Symbology" version="3.34.4-Prizren">
  <pipe-data-defined-properties>
    <Option type="Map">
      <Option value="" type="QString" name="name"/>
      <Option name="properties"/>
      <Option value="collection" type="QString" name="type"/>
    </Option>
  </pipe-data-defined-properties>
  <pipe>
    <provider>
      <resampling zoomedOutResamplingMethod="nearestNeighbour" zoomedInResamplingMethod="nearestNeighbour" enabled="false" maxOversampling="2"/>
    </provider>
    <rasterrenderer classificationMin="3.1466175" classificationMax="24.564434" opacity="1" band="1" type="singlebandpseudocolor" nodataColor="" alphaBand="-1">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>MinMax</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader minimumValue="3.1466175000000001" clip="0" colorRampType="INTERPOLATED" maximumValue="24.564433999999999" classificationMode="1" labelPrecision="4">
          <colorramp type="gradient" name="[source]">
            <Option type="Map">
              <Option value="26,150,65,255" type="QString" name="color1"/>
              <Option value="215,25,28,255" type="QString" name="color2"/>
              <Option value="cw" type="QString" name="direction"/>
              <Option value="0" type="QString" name="discrete"/>
              <Option value="gradient" type="QString" name="rampType"/>
              <Option value="rgb" type="QString" name="spec"/>
              <Option value="0.25;166,217,106,255;rgb;cw:0.5;255,255,192,255;rgb;cw:0.75;253,174,97,255;rgb;cw" type="QString" name="stops"/>
            </Option>
          </colorramp>
          <item value="3.1466175" label="3,1466" alpha="255" color="#1a9641"/>
          <item value="8.501071625" label="8,5011" alpha="255" color="#a6d96a"/>
          <item value="13.855525749999998" label="13,8555" alpha="255" color="#ffffc0"/>
          <item value="19.209979875" label="19,2100" alpha="255" color="#fdae61"/>
          <item value="24.564434" label="24,5644" alpha="255" color="#d7191c"/>
          <rampLegendSettings maximumLabel="" minimumLabel="" direction="0" suffix="" orientation="2" useContinuousLegend="1" prefix="">
            <numericFormat id="basic">
              <Option type="Map">
                <Option type="invalid" name="decimal_separator"/>
                <Option value="6" type="int" name="decimals"/>
                <Option value="0" type="int" name="rounding_type"/>
                <Option value="false" type="bool" name="show_plus"/>
                <Option value="true" type="bool" name="show_thousand_separator"/>
                <Option value="false" type="bool" name="show_trailing_zeros"/>
                <Option type="invalid" name="thousand_separator"/>
              </Option>
            </numericFormat>
          </rampLegendSettings>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast gamma="1" contrast="0" brightness="0"/>
    <huesaturation colorizeStrength="100" saturation="0" invertColors="0" colorizeRed="255" colorizeOn="0" colorizeGreen="128" grayscaleMode="0" colorizeBlue="128"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
