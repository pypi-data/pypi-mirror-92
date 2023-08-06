define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'

    , '../../api.js'    
    , '../../constData.js'
    , '../base/index.js'
], function ( $, vpCommon, vpConst, sb, 
            //   block
              api
              , constData
              , baseComponent ) {


    const { MakeOptionContainer } = baseComponent;
    var InitElseBlockOption = function(thisBlock, optionPageSelector) {
        var renderThisComponent = function() {
            var elseBlockOption = MakeOptionContainer(thisBlock);
            elseBlockOption.append('<div>(N/A)</div>');

            /**block option 탭에 렌더링된 dom객체 생성 */
            $(optionPageSelector).append(elseBlockOption);
            
            return elseBlockOption;
        }
        return renderThisComponent();
    }

    return InitElseBlockOption;
});