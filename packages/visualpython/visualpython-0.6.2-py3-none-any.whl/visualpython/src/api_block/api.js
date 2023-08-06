define([
    'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'

    , './constData.js'
], function ( vpCommon, vpConst, sb,
              constData ) {

    const { BLOCK_GROUP_TYPE
            , BLOCK_CODELINE_TYPE
            , BLOCK_DIRECTION
            , IMPORT_BLOCK_TYPE
            , IF_BLOCK_CONDITION_TYPE
            , FOCUSED_PAGE_TYPE
            
            , DEF_BLOCK_ARG4_TYPE

            , FOR_BLOCK_ARG3_TYPE
            , WHILE_BLOCK_TYPE 

            , STR_GRP_DEFINE
            , STR_GRP_CONTROL
            , STR_GRP_EXECUTE

            , STR_CLASS
            , STR_DEF
            , STR_IF
            , STR_FOR
            , STR_WHILE
            , STR_IMPORT
            , STR_API
            , STR_TRY
            , STR_EXCEPT
            , STR_FINALLY
            , STR_RETURN
            , STR_BREAK
            , STR_CONTINUE
            , STR_PASS
            , STR_PROPERTY
            , STR_CODE
            , STR_LAMBDA
            , STR_COMMENT
            , STR_NODE
            , STR_TEXT
            , STR_PRINT
            , STR_ELIF
            , STR_ELSE
            , STR_FOCUS
            , STR_BLUR
            , STR_INPUT
        
            , STR_EMPTY

            , STR_INPUT_YOUR_CODE
            , STR_TRANSPARENT
            , STR_COLOR
            , STR_BACKGROUND_COLOR
            , STR_KEYWORD_NEW_LINE

            , VP_ID_PREFIX 
            , VP_ID_APIBLOCK_LEFT_TAP_APILIST_PAGE

            , VP_CLASS_PREFIX 
 
            , VP_BLOCK_BLOCKCODELINETYPE_CODE
            , VP_BLOCK_BLOCKCODELINETYPE_CLASS_DEF
            , VP_BLOCK_BLOCKCODELINETYPE_CONTROL
 
            , VP_CLASS_BLOCK_CODETYPE_NAME
            , VP_CLASS_APIBLOCK_BOARD
            , VP_CLASS_APIBLOCK_BUTTONS
            , VP_CLASS_APIBLOCK_OPTION_TAB
            , VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED
            , VP_CLASS_APIBLOCK_PARAM_PLUS_BTN
            , VP_CLASS_APIBLOCK_BODY 

            , STATE_classInParamList
            , STATE_className
            , STATE_parentClassName
            
            , STATE_defName
            , STATE_defInParamList
            , STATE_defReturnType

            , STATE_ifCodeLine
            , STATE_isIfElse
            , STATE_isForElse
            , STATE_ifConditionList
            , STATE_elifConditionList
 
            , STATE_elifCodeLine
            , STATE_elifList
 
            , STATE_forCodeLine
            , STATE_forParam 
            , STATE_listforConditionList
            , STATE_listforReturnVar
            , STATE_listforPrevExpression
 
            , STATE_whileCodeLine
            , STATE_whileBlockOptionType
            , STATE_whileArgs
            , STATE_whileConditionList

            , STATE_breakCodeLine
            , STATE_passCodeLine
            , STATE_continueCodeLine
 
            , STATE_baseImportList
            , STATE_customImportList
 
            , STATE_exceptList
            , STATE_exceptCodeLine
            , STATE_exceptConditionList
 
            , STATE_isFinally
 
            , STATE_returnOutParamList
 
            , STATE_codeLine
 
            , STATE_propertyCodeLine
 
            , STATE_commentLine
 
            , STATE_lambdaArg1
            , STATE_lambdaArg2List
            , STATE_lambdaArg2m_List
            , STATE_lambdaArg3
            , STATE_lambdaArg4List
 
            , COLOR_GRAY_input_your_code
            , COLOR_FOCUSED_PAGE
            , COLOR_BLACK   } = constData;

    /** CreateOneArrayValueAndGet
        *  배열의 특정 인덱스 값을 생성하고 새로운 배열을 리턴한다
        *  @param {Array} array 
        *  @param {number} index
        *  @param {number | string} newValue 
        *  @returns {Array} New array
        */
    var CreateOneArrayValueAndGet = function(array, index, newValue) {
        return [ ...array.slice(0, index+1), newValue,
                 ...array.slice(index+1, array.length) ]
    }

    /** UpdateOneArrayValueAndGet
        *  배열의 특정 인덱스 값을 업데이트하고 업데이트된 새로운 배열을 리턴한다
        *  @param {Array} array 
        *  @param {number} index
        *  @param {number | string} newValue 
        *  @returns {Array} New array
        */
    var UpdateOneArrayValueAndGet = function(array, index, newValue) {
        return [ ...array.slice(0, index), newValue,
                 ...array.slice(index+1, array.length) ]
    }

    /** DeleteOneArrayValueAndGet
    *  배열의 특정 인덱스 값을 삭제하고 삭제된 새로운 배열을 리턴한다
    *  @param {Array} array 
    *  @param {number} index 
    *  @returns {Array} New array
    */
    var DeleteOneArrayValueAndGet = function(array, index) {
        return [ ...array.slice(0, index), 
                 ...array.slice(index+1, array.length) ]
    }
    
    /** API Block에서 자체적으로 input을 제어하기 위한 api */
    var ControlToggleInput = function() {
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BODY)).on(STR_FOCUS, STR_INPUT, function() {
            Jupyter.notebook.keyboard_manager.disable();
        });
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BODY)).on(STR_BLUR, STR_INPUT, function() {
            Jupyter.notebook.keyboard_manager.enable();
        });
    }

    /** 그룹 type에 따라 이름을 리턴하는 함수 */
    var MapGroupTypeToName = function(type) {
        var name = '';
        switch (type) {
            case BLOCK_GROUP_TYPE.DEFINE: {
                name = STR_GRP_DEFINE;
                break;
            }
            case BLOCK_GROUP_TYPE.CONTROL: {
                name = STR_GRP_CONTROL;
                break;
            }
            case BLOCK_GROUP_TYPE.EXECUTE: {
                name = STR_GRP_EXECUTE;
                break;
            }
        }
        return name;
    }

    /** 블럭 type에 따른 이름을 리턴하는 함수 */
    var MapTypeToName = function(type) {
        var name = ``;
        switch (type) {
            case BLOCK_CODELINE_TYPE.CLASS: {
                name = STR_CLASS;
                break;
            }
            case BLOCK_CODELINE_TYPE.DEF: {
                name = STR_DEF;
                break;
            }
            case BLOCK_CODELINE_TYPE.IF: {
                name = STR_IF;
                break;
            }
            case BLOCK_CODELINE_TYPE.ELIF: {
                name = STR_ELIF;
                break;
            }
            case BLOCK_CODELINE_TYPE.ELSE: {
                name = STR_ELSE;
                break;
            }
            case BLOCK_CODELINE_TYPE.FOR: {
                name = STR_FOR;
                break;
            }
            case BLOCK_CODELINE_TYPE.FOR_ELSE: {
                name = STR_ELSE;
                break;
            }
            case BLOCK_CODELINE_TYPE.WHILE: {
                name = STR_WHILE;
                break;
            }
            case BLOCK_CODELINE_TYPE.IMPORT: {
                name = STR_IMPORT;
                break;
            }
            case BLOCK_CODELINE_TYPE.API: {
                name = STR_API;
                break;
            }
            case BLOCK_CODELINE_TYPE.TRY: {
                name = STR_TRY;
                break;
            }
            case BLOCK_CODELINE_TYPE.EXCEPT: {
                name = STR_EXCEPT;
                break;
            }
            case BLOCK_CODELINE_TYPE.FINALLY: {
                name = STR_FINALLY;
                break;
            }
            case BLOCK_CODELINE_TYPE.RETURN: {
                name = STR_RETURN;
                break;
            }
            case BLOCK_CODELINE_TYPE.BREAK: {
                name = STR_BREAK;
                break;
            }
            case BLOCK_CODELINE_TYPE.CONTINUE: {
                name = STR_CONTINUE;
                break;
            }
            case BLOCK_CODELINE_TYPE.PASS: {
                name = STR_PASS;
                break;
            }
            case BLOCK_CODELINE_TYPE.PROPERTY: {
                name = STR_PROPERTY;
                break;
            }
            case BLOCK_CODELINE_TYPE.CODE: {
                name = STR_CODE;
                break;
            }
            case BLOCK_CODELINE_TYPE.LAMBDA: {
                name = STR_LAMBDA;
                break;
            }
            case BLOCK_CODELINE_TYPE.COMMENT: {
                name = STR_COMMENT;
                break;
            }
            case BLOCK_CODELINE_TYPE.PRINT: {
                name = STR_PRINT;
                break;
            }
            case BLOCK_CODELINE_TYPE.NODE: {
                name = STR_NODE;
                break;
            }
            case BLOCK_CODELINE_TYPE.TEXT: {
                name = STR_TEXT;
                break;
            }
            case BLOCK_CODELINE_TYPE.HOLDER: {
                name = '';
                break;
            }
            default: {
                break;
            }
        }
        return name;
    }

    var RemoveSomeBlockAndGetBlockList = function(allArray, exceptArray) {
        var lastArray = [];
        allArray.forEach((block) => {
            var is = exceptArray.some((exceptBlock) => {
                if ( block.getUUID() == exceptBlock.getUUID() ) {
                    return true;
                } 
            });

            if (is !== true) {
                lastArray.push(block);
            } 
        });
        return lastArray;
    }
    
    var SetChildBlockList_down_first_indent_last = function( stack, blockList ) {
        /** block데이터를 배열에 담을때 INDENT 타입과 DOWN 타입의 위치 변경
         *  DOWN 앞으로, INDENT 뒤로
         */
        blockList = blockList.sort((block1, block2) => {
            if (block1.getDirection() == BLOCK_DIRECTION.INDENT) {
                return 1;
            } else {
                return -1;
            }
        });
        blockList.forEach(el => {
            stack.unshift(el);
        });  
        return stack;  
    }

    /** */
    var MapNewLineStrToIndentString = function(str, indentString) {
        var _str = str.replace(/(\r\n\t|\n|\r\t)/gm,`\n${indentString}`);
        return _str;
    }

    /**
     * 텍스트 박스 라인 넘버 설정
     * @vpCommon_custom
     * @param {object} trigger 이벤트 트리거 객체
     */
    var SetTextareaLineNumber_apiBlock = function(trigger, textareaValue) {
        var rowCnt = textareaValue.split('\n').length;
        var sbLineText = new sb.StringBuilder();

        for (var idx = 1; idx <= rowCnt; idx++) {
            sbLineText.appendLine(idx);
        }

        $(trigger).prev(vpCommon.formatString(".{0}", vpConst.MANUAL_CODE_INPUT_AREA_LINE)).val(sbLineText.toString());
    }

    /** class param 생성 */
    var GenerateClassInParamList = function(thatBlock) {
        var parentClassName = thatBlock.getState(STATE_parentClassName);
        var classInParamStr = `(`;
        classInParamStr += parentClassName;
        classInParamStr += `):`;
        return classInParamStr;
    }
 
    /** def param 생성 */
    var GenerateDefInParamList = function(thatBlock) {
         /** 함수 파라미터 */
         var defInParamList = thatBlock.getState(STATE_defInParamList);
         var defReturnTypeState = thatBlock.getState(STATE_defReturnType);
         var defInParamStr = `(`;
         defInParamList.forEach(( defInParam, index ) => {
            const { arg3, arg4, arg5 ,arg6 } = defInParam;
                 
            if (arg6 == '*args') {
                defInParamStr += '*';
            } else if (arg6 == '**kwargs') {
                defInParamStr += '**';
            }
 
            defInParamStr += arg3;
 
            if (arg4 == DEF_BLOCK_ARG4_TYPE.NONE || arg4 == STR_EMPTY) {
                defInParamStr += '';
            } else {
                   
                if (arg4 != DEF_BLOCK_ARG4_TYPE.INPUT_STR) {
                    defInParamStr += ':';
                    defInParamStr += arg4;
                } 
            }
 
            if (arg5 !== '') {
                defInParamStr += `=${arg5}`;
            }
 
            for (var i = index + 1; i < defInParamList.length; i++) {
                if (defInParamList[i].arg3 !== '') {
                    defInParamStr += `, `;
                    break;
                }
            };
         });
         defInParamStr += `)`;

         if (defReturnTypeState == DEF_BLOCK_ARG4_TYPE.NONE || defReturnTypeState == STR_EMPTY) {
            defInParamStr += `:`;
         } else {
            if (defReturnTypeState != DEF_BLOCK_ARG4_TYPE.INPUT_STR) {
                defInParamStr += ` `;
                defInParamStr += `->`;
                defInParamStr += ` `;
                defInParamStr += defReturnTypeState;
                defInParamStr += `:`;
            } 
         }
 
         return defInParamStr;
    }
 
    /** return param 생성 */
    var GenerateReturnOutParamList = function(thatBlock) {
        var returnOutParamList = thatBlock.getState(STATE_returnOutParamList);
        var returnOutParamStr = ` `;
        returnOutParamList.forEach(( returnInParam, index ) => {
            if (returnInParam !== '' ) {
                returnOutParamStr += `${returnInParam}`;
                for (var i = index + 1; i < returnOutParamList.length; i++) {
                    if (returnOutParamList[i] !== '') {
                        returnOutParamStr += `, `;
                        break;
                    }
                };
            }
        });
        returnOutParamStr += ``;
        return returnOutParamStr;
    }
 
    /** if param 생성 */
    var GenerateIfConditionList = function(thatBlock, blockCodeLineType) {
         var ifConditionList;
         if (blockCodeLineType == BLOCK_CODELINE_TYPE.IF) {
             ifConditionList = thatBlock.getState(STATE_ifConditionList);
         } else {
             ifConditionList = thatBlock.getState(STATE_elifConditionList);
         }
 
         var ifConditionListStr = ``;
         ifConditionList.forEach(( ifCondition, index ) => {
             const { conditionType } = ifCondition;
             if (conditionType == IF_BLOCK_CONDITION_TYPE.ARG) {
                const { arg1, arg2, arg3, arg4, arg5, arg6 } = ifCondition;

                if ( !(arg1 == '' && (arg2 == 'none' || arg2 == '') && arg3 == '')) {
                    ifConditionListStr += `(`;
                }
                ifConditionListStr += arg1;
  
                if ( arg2 !== 'none' ) {
                    ifConditionListStr += arg2;
                }
                ifConditionListStr += arg3;
         
                if ( arg4 !== 'none' ) {
                    ifConditionListStr += arg4;
                    ifConditionListStr += arg5;
                }
                 
                if ( !(arg1 == '' && (arg2 == 'none' || arg2 == '') && arg3 == '')) {
                    ifConditionListStr += `)`;
                }
         
                if ( ifConditionList.length -1 !== index ) {
                    ifConditionListStr += '';
                    ifConditionListStr += arg6;
                    ifConditionListStr += '';
                }
            } else {
                const { codeLine, arg6 } = ifCondition;
                if (codeLine == '') {
                    return;
                }
                ifConditionListStr += `(`;
                ifConditionListStr += codeLine;
                ifConditionListStr += `)`;
 
                if ( ifConditionList.length -1 !== index ) {
                    ifConditionListStr += '';
                    ifConditionListStr += arg6;
                    ifConditionListStr += '';
                }
            }
        });
 
        return ifConditionListStr;
    }
 
      /** while param 생성 */
    var GenerateWhileConditionList = function(thatBlock) {
        var ifConditionList = thatBlock.getState(STATE_whileConditionList);
 

        var ifConditionListStr = ``;
        ifConditionList.forEach(( ifCondition, index ) => {
            // const { conditionType } = ifCondition;
            // if (conditionType == IF_BLOCK_CONDITION_TYPE.ARG) {
                const { arg1, arg2, arg3, arg4, arg5, arg6 } = ifCondition;

               if ( !(arg1 == '' && (arg2 == 'none' || arg2 == '') && arg3 == '')) {
                   ifConditionListStr += `(`;
               }

                ifConditionListStr += arg1;
 
                if ( arg2 !== 'none' ) {
                   ifConditionListStr += arg2;
                }
                ifConditionListStr += arg3;
        
                if ( arg4 !== 'none' ) {
                    ifConditionListStr += arg4;
                    ifConditionListStr += arg5;
                }
                
                if ( !(arg1 == '' && (arg2 == 'none' || arg2 == '') && arg3 == '')) {
                   ifConditionListStr += `)`;
               }
        
                if ( ifConditionList.length -1 !== index ) {
                    ifConditionListStr += '';
                    ifConditionListStr += arg6;
                    ifConditionListStr += '';
                }
            // } else {
                // const { codeLine, arg6 } = ifCondition;
                // if (codeLine == '') {
                //     return;
                // }
                // ifConditionListStr += `(`;
                // ifConditionListStr += codeLine;
                // ifConditionListStr += `)`;

                // if ( ifConditionList.length -1 !== index ) {
                //     ifConditionListStr += '';
                //     ifConditionListStr += arg6;
                //     ifConditionListStr += '';
                // }
            // }

        });

       return ifConditionListStr;
    }
     var GenerateExceptConditionList = function(thatBlock) {
         var exceptConditionList = thatBlock.getState(STATE_exceptConditionList);
 
         var exceptConditionListStr = ``;
         exceptConditionList.forEach(( exceptCondition, index ) => {
            const { conditionType } = exceptCondition;
            if (conditionType == IF_BLOCK_CONDITION_TYPE.ARG) {
                const { arg1, arg2, arg3 } = exceptCondition;
        
                exceptConditionListStr += arg1;

                if ( arg2 == 'none' || arg2 == STR_EMPTY ) {
                } else {
                    exceptConditionListStr += ' ';
                    exceptConditionListStr += arg2;
                    exceptConditionListStr += ' ';
                    exceptConditionListStr += arg3;
                }
        
            } else {
                const { codeLine } = exceptCondition;
                if (codeLine == '') {
                    return;
                }
             
                exceptConditionListStr += codeLine;
            }
     
         });
 
        return exceptConditionListStr;
     }
 
     /** for param 생성 */
     var GenerateForParam = function(thatBlock) {
         var forParam = thatBlock.getState(STATE_forParam);
         const { arg1, arg2, arg3, arg4, arg5, arg6, arg7 } = forParam;
 
         var forParamStr = ``;
 
         if (arg1 !== STR_EMPTY) {
             forParamStr += arg1;
             forParamStr += ' ';
         }
 
         if (arg3 == FOR_BLOCK_ARG3_TYPE.ENUMERATE && arg1 !== STR_EMPTY && arg4 !== STR_EMPTY) { 
             forParamStr += ',';
         }
 
         if (arg3 == FOR_BLOCK_ARG3_TYPE.ENUMERATE && arg4 !== STR_EMPTY) {
             forParamStr += arg4;
             forParamStr += ' ';
         }
 
         forParamStr += 'in';
         forParamStr += ' ';
 
         if (arg3 == FOR_BLOCK_ARG3_TYPE.ZIP) {
             forParamStr += arg3;
             forParamStr += '(';
             forParamStr += arg2;
 
             if (arg7 !== '') {
                 forParamStr += ',';
                 forParamStr += ' ';
                 forParamStr += arg7;
             }
 
             forParamStr += ')';
 
         } else if (arg3 ==  FOR_BLOCK_ARG3_TYPE.ENUMERATE ) {
             forParamStr += arg3;
             forParamStr += '(';
             forParamStr += arg2;
             forParamStr += ')';
 
         } else if (arg3 ==  FOR_BLOCK_ARG3_TYPE.RANGE ) {
             forParamStr += arg3;
             forParamStr += '(';
 
             if (arg5 !== '') {
                 forParamStr += arg5;
             }
 
             if (arg5 !== '' && arg2 !== '') { 
                 forParamStr += ',';
             }
 
             if (arg2 !== '') {
                 forParamStr += ' ';
                 forParamStr += arg2;
             }
 
             if ((arg5 !== '' || arg2 !== '') && arg6 !== '') { 
                 forParamStr += ',';
             }
 
             if (arg6 !== '') {
                 forParamStr += ' ';
                 forParamStr += arg6;
             }
   
             forParamStr += ')';
 
         } else {
            if (arg3 != FOR_BLOCK_ARG3_TYPE.INPUT_STR) {
                forParamStr += arg3;
            } 

            if (arg2 != '') {
                if (arg3 == '' || arg3 == FOR_BLOCK_ARG3_TYPE.INPUT_STR) {
                    forParamStr += arg2;
                } else {
                    forParamStr += '(';
                    forParamStr += arg2;
                    forParamStr += ')';
                }
            }

         }

         return forParamStr;
     }
 
     /** Listfor param 생성 */
     var GenerateListforConditionList = function(thatBlock) {
         var listforStr = '';
         var listforReturnVar = thatBlock.getState(STATE_listforReturnVar);
         var listforPrevExpression = thatBlock.getState(STATE_listforPrevExpression);
 
         if (listforReturnVar != '') {
             listforStr += listforReturnVar;
             listforStr += ' ';
             listforStr += '=';
             listforStr += ' ';
         }
 
         listforStr += '[';
         listforStr += listforPrevExpression;
 
 
         var listforConditionList = thatBlock.getState(STATE_listforConditionList);
         listforConditionList.forEach(listforCondition => {
             const { arg1, arg2, arg3, arg4, arg5, arg6, arg7
                     , arg10, arg11, arg12, arg13, arg14, arg15  } = listforCondition;
 
             listforStr += ' ';
             listforStr += 'for';
             listforStr += ' ';
             if (arg1 !== '') {
                 listforStr += arg1;
                 listforStr += ' ';
             }
     
             if (arg3 == 'enumerate' && arg1 !== '' && arg4 !== '') { 
                 listforStr += ',';
             }
     
             if (arg3 == 'enumerate' && arg4 !== '') {
                 listforStr += arg4;
                 listforStr += ' ';
             }
     
             listforStr += 'in';
             listforStr += ' ';
     
             if (arg3 == 'zip') {
                 listforStr += arg3;
                 listforStr += '(';
                 listforStr += arg2;
     
                 if (arg7 !== '') {
                     listforStr += ',';
                     listforStr += ' ';
                     listforStr += arg7;
                 }
     
                 listforStr += ')';
     
             } else if (arg3 == 'enumerate') {
                 listforStr += arg3;
                 listforStr += '(';
                 listforStr += arg2;
                 listforStr += ')';
     
             } else if (arg3 == 'range') {
                 listforStr += arg3;
                 listforStr += '(';
     
                 if (arg5 !== '') {
                     listforStr += arg5;
                 }
     
                 if (arg5 !== '' && arg2 !== '') { 
                     listforStr += ',';
                 }
     
                 if (arg2 !== '') {
                     listforStr += ' ';
                     listforStr += arg2;
                 }
     
                 if ((arg5 !== '' || arg2 !== '') && arg6 !== '') { 
                     listforStr += ',';
                 }
     
                 if (arg6 !== '') {
                     listforStr += ' ';
                     listforStr += arg6;
                 }
       
                 listforStr += ')';
     
             } 

            else {
                if (arg3 != FOR_BLOCK_ARG3_TYPE.INPUT_STR) {
                    listforStr += arg3;
                } 
    
                if (arg2 != '') {
                    if (arg3 == '' || arg3 == FOR_BLOCK_ARG3_TYPE.INPUT_STR) {
                        listforStr += arg2;
                    } else {
                        listforStr += '(';
                        listforStr += arg2;
                        listforStr += ')';
                    }
                }
            }
 
            if (arg10 == 'if') {
                listforStr += ' ';
                listforStr += 'if';
                listforStr += ' ';
                listforStr += `(`;
         
                listforStr += arg11;
                listforStr += arg12;
                listforStr += arg13;
         
                if ( arg14 !== 'none' ) {
                    listforStr += arg14;
                    listforStr += arg15;
                }
                 
                listforStr += ' ';
                listforStr += `)`;
                listforStr += '';
     
            } else if (arg10 == 'inputStr') {
 
            }
        });
 
        listforStr += ']';
        return listforStr;
     }
 
    var GenerateLambdaParamList = function(thatBlock) {
        var lambdaParamStr = STR_EMPTY;
        var lambdaArg1State = thatBlock.getState(STATE_lambdaArg1);
        var lambdaArg2ListState = thatBlock.getState(STATE_lambdaArg2List);
        var lambdaArg3State = thatBlock.getState(STATE_lambdaArg3);

        if (lambdaArg1State != '') {
            lambdaParamStr += lambdaArg1State;
            lambdaParamStr += ' ';
            lambdaParamStr += '=';
            lambdaParamStr += ' ';
        }
 
        lambdaParamStr += 'lambda';
        lambdaParamStr += ' ';
        lambdaArg2ListState.forEach( (lambdaArg2, index) => {
            lambdaParamStr += lambdaArg2;
            if ( lambdaArg2ListState.length - 1 != index) {
                if (lambdaArg2 != '') {
                    lambdaParamStr += ' ';
                    lambdaParamStr += ',';
                }
            }
        });
   
        lambdaParamStr += ':';  
        lambdaParamStr += MapNewLineStrToIndentString(lambdaArg3State);
   
        return lambdaParamStr;
     }

     var GenerateImportList = function(thisBlock, indentString) {
        var codeLine = STR_EMPTY;
        var blockName = 'import';
        var baseImportList = thisBlock.getState(STATE_baseImportList).filter(baseImport => {
            if ( baseImport.isImport == true) {
                return true;
            } else {
                return false;
            }
        });

        var customImportList = thisBlock.getState(STATE_customImportList).filter(customImport => {
            if ( customImport.isImport == true) {
                return true;
            } else {
                return false;
            }
        });
   
        var lineNum = 0;
        var indentString = thisBlock.getIndentString();

        baseImportList.forEach((baseImport, index) => {
            if (lineNum > 0) {
                codeLine += indentString;
            } 
      
            codeLine += `${blockName.toLowerCase()} ${baseImport.baseImportName} as ${baseImport.baseAcronyms}`;
            if (baseImport.baseImportName == 'matplotlib.pyplot') {
                codeLine += STR_KEYWORD_NEW_LINE;
                codeLine += indentString;
                codeLine += `%matplotlib inline`;
            }

            if (index != baseImportList.length - 1) {
                codeLine += STR_KEYWORD_NEW_LINE;
            }
            lineNum++;
        });

        customImportList.forEach((customImport,index ) => {
            if (lineNum > 0) {
                codeLine += indentString;
            } 

            codeLine += `${blockName.toLowerCase()} ${customImport.baseImportName} as ${customImport.baseAcronyms}`;
            if (customImport.baseImportName == 'matplotlib.pyplot') {
                codeLine += STR_KEYWORD_NEW_LINE;
                codeLine += indentString;
                codeLine += `%matplotlib inline`;
            }

            if (index != customImportList.length - 1) {
                codeLine += STR_KEYWORD_NEW_LINE;
            }

            lineNum++;
        });

        // console.log(codeLine);
        return codeLine;
     };

     var GenerateWhileBlockCode = function(thisBlock) {
        var whileBlockCode = STR_EMPTY;
        var whileArgsState = thisBlock.getState(STATE_whileArgs)
        var whileBlockOptionType = thisBlock.getState(STATE_whileBlockOptionType);
        const { arg1, arg2, arg3, arg4, arg5 } = whileArgsState;

        if (whileBlockOptionType == WHILE_BLOCK_TYPE.CONDITION) {
            whileBlockCode += arg4;
            whileBlockCode += arg2;
            whileBlockCode += arg3;
        } else if (whileBlockOptionType == WHILE_BLOCK_TYPE.TRUE_FALSE) {
            whileBlockCode += arg1;
        } else {
            whileBlockCode += arg1;
        }
        return whileBlockCode;
     }

     var ShowImportListAtBlock = function(thisBlock) {
        var codeLine = STR_EMPTY;
        var baseImportList = thisBlock.getState(STATE_baseImportList).filter(baseImport => {
            if ( baseImport.isImport == true) {
                return true;
            } else {
                return false;
            }
        });
        var customImportList = thisBlock.getState(STATE_customImportList).filter(customImport => {
            if ( customImport.isImport == true) {
                return true;
            } else {
                return false;
            }
        });

        if (baseImportList.length != 0) {
            codeLine += baseImportList[0].baseImportName + ' as ' + baseImportList[0].baseAcronyms;
        } else if (customImportList.length != 0) {
            codeLine += customImportList[0].baseImportName + ' as ' + customImportList[0].baseAcronyms;
        }
        // console.log('codeLine',codeLine);
        return codeLine;
    }
    
    /**  멀티라인의 첫번째 줄만 보여준다 */
    var ShowCodeBlockCode = function(thisBlock) {
        var codeLine = thisBlock.getState(STATE_codeLine);
        var firstNewLine_index = codeLine.indexOf('\n');
        if (firstNewLine_index != -1) {
            var sliced_codeline = codeLine.slice(0, firstNewLine_index);
            return sliced_codeline;
        } else {
            return codeLine;
        }
    }
    

 
    /** 특정 input태그 값 입력 안 될시 빨간색 border 
     */
    var RenderInputRequiredColor = function(thatBlock) {
        if ($(thatBlock).val() == STR_EMPTY) {
            $(thatBlock).addClass(VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED)
        } else {
            $(thatBlock).removeClass(VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED); 
        }
    }
 
    var RenderSelectRequiredColor = function(target, selectedValue) {
        if (selectedValue == STR_EMPTY) {
            $(target).addClass(VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED)
        } else {
            $(target).removeClass(VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED); 
        }
    }
 
 
    /**
     * @param {string} inputValue 
     */
    var RenderCodeBlockInputRequired = function(thisBlock, inputValue, state) {
        /** 어떤 데이터도 입력되지 않을 때 */
        if (inputValue == STR_EMPTY) {
            thisBlock.writeCode(STR_INPUT_YOUR_CODE);
            $(`.vp-block-header-${thisBlock.getUUID()}`).css(STR_COLOR, COLOR_GRAY_input_your_code);
            return;
        }
 
        /** 데이터가 입력되었을 때 */
        thisBlock.writeCode(state);
        $(`.vp-block-header-${thisBlock.getUUID()}`).css(STR_COLOR, COLOR_BLACK);
    }
 
     var RenderHTMLDomColor = function(block, htmlDom) {
         var blockType = block.getBlockType();
 
         /** class & def 블럭 */
         if ( blockType == BLOCK_CODELINE_TYPE.CLASS 
             || blockType == BLOCK_CODELINE_TYPE.DEF) {
             $(htmlDom).addClass(VP_BLOCK_BLOCKCODELINETYPE_CLASS_DEF);
             
         /** controls 블럭 */
         } else if ( blockType == BLOCK_CODELINE_TYPE.IF 
             || blockType == BLOCK_CODELINE_TYPE.FOR
             || blockType == BLOCK_CODELINE_TYPE.WHILE 
             || blockType == BLOCK_CODELINE_TYPE.TRY
             || blockType == BLOCK_CODELINE_TYPE.ELSE 
             || blockType == BLOCK_CODELINE_TYPE.ELIF
             || blockType == BLOCK_CODELINE_TYPE.FOR_ELSE 
             || blockType == BLOCK_CODELINE_TYPE.EXCEPT 
             || blockType == BLOCK_CODELINE_TYPE.FINALLY 
             || blockType == BLOCK_CODELINE_TYPE.IMPORT
             || blockType == BLOCK_CODELINE_TYPE.LAMBDA
             || blockType == BLOCK_CODELINE_TYPE.PROPERTY ) {
             //  COLOR_CONTROL;
             $(htmlDom).addClass(VP_BLOCK_BLOCKCODELINETYPE_CONTROL);
 
         } else if (blockType == BLOCK_CODELINE_TYPE.BLANK){
             $(htmlDom).css(STR_BACKGROUND_COLOR, STR_TRANSPARENT);
    
         }  else if (blockType == BLOCK_CODELINE_TYPE.TEXT) {
            $(htmlDom).css(STR_BACKGROUND_COLOR, STR_TRANSPARENT);
         } else if (blockType == BLOCK_CODELINE_TYPE.HOLDER ) {

         } else {
             $(htmlDom).addClass(VP_BLOCK_BLOCKCODELINETYPE_CODE);
         }
         return htmlDom;
    }
 


    var IsCanHaveIndentBlock = function(blockType) {
        if ( blockType == BLOCK_CODELINE_TYPE.CLASS
            || blockType == BLOCK_CODELINE_TYPE.DEF

            || blockType == BLOCK_CODELINE_TYPE.IF 
            || blockType == BLOCK_CODELINE_TYPE.FOR
            || blockType == BLOCK_CODELINE_TYPE.TRY
            || blockType == BLOCK_CODELINE_TYPE.WHILE
            
            || blockType == BLOCK_CODELINE_TYPE.ELSE 
            || blockType == BLOCK_CODELINE_TYPE.ELIF
            || blockType == BLOCK_CODELINE_TYPE.FOR_ELSE 
            || blockType == BLOCK_CODELINE_TYPE.EXCEPT 
            || blockType == BLOCK_CODELINE_TYPE.FINALLY ) {
           return true;
       } else {
           return false;
       }
    }

    var IsCodeBlockType = function(blockType) {
        if ( blockType == BLOCK_CODELINE_TYPE.CODE
            || blockType == BLOCK_CODELINE_TYPE.PASS
            || blockType == BLOCK_CODELINE_TYPE.CONTINUE 
            || blockType == BLOCK_CODELINE_TYPE.BREAK
            || blockType == BLOCK_CODELINE_TYPE.PROPERTY
            || blockType == BLOCK_CODELINE_TYPE.PRINT
            
            || blockType == BLOCK_CODELINE_TYPE.BLANK
            || blockType == BLOCK_CODELINE_TYPE.COMMENT  ) {
            return true;
        } else {
            return false;
        }
    }

    var IsElifElseExceptFinallyBlockType = function(blockType) {
        if ( blockType == BLOCK_CODELINE_TYPE.ELIF
            || blockType == BLOCK_CODELINE_TYPE.EXCEPT
            || blockType == BLOCK_CODELINE_TYPE.ELSE 
            || blockType == BLOCK_CODELINE_TYPE.FOR_ELSE
            || blockType == BLOCK_CODELINE_TYPE.FINALLY  ) {
            return true;
        } else {
            return false;
        }
    }

    var IsIfForTryBlockType = function(blockType) {
        if ( blockType == BLOCK_CODELINE_TYPE.IF
            || blockType == BLOCK_CODELINE_TYPE.FOR
            || blockType == BLOCK_CODELINE_TYPE.TRY) {
            return true;
        } else {
            return false;
        }
    }

    var IsNodeTextBlockType = function(blockType) {
        if ( blockType == BLOCK_CODELINE_TYPE.NODE
             || blockType == BLOCK_CODELINE_TYPE.TEXT) {
             return true;
        } else {
            return false;
        }
    }

    var IsDefineBlockType = function(blockType) {
        if ( blockType == BLOCK_CODELINE_TYPE.CLASS
             || blockType == BLOCK_CODELINE_TYPE.DEF) {
             return true;
        } else {
            return false;
        }
    }

    var IsControlBlockType = function(blockType) {
        if ( blockType == BLOCK_CODELINE_TYPE.IF 
            || blockType == BLOCK_CODELINE_TYPE.FOR
            || blockType == BLOCK_CODELINE_TYPE.WHILE 
            || blockType == BLOCK_CODELINE_TYPE.TRY

            || blockType == BLOCK_CODELINE_TYPE.CONTINUE
            || blockType == BLOCK_CODELINE_TYPE.BREAK
            || blockType == BLOCK_CODELINE_TYPE.PASS
            || blockType == BLOCK_CODELINE_TYPE.RETURN) {
             return true;
        } else {
            return false;
        }
    }

       /**
     * types에 해당하는 데이터유형을 가진 변수 목록 조회
     * @param {*} types 조회할 변수들의 데이터유형 목록
     * @param {*} callback 조회 후 실행할 callback. parameter로 result를 받는다
     */

    var LoadVariableList = function(blockContainer) {
        var types = [
            // pandas 객체
            'DataFrame', 'Series', 'Index', 'Period', 'GroupBy', 'Timestamp'
            // Index 하위 유형
            , 'RangeIndex', 'CategoricalIndex', 'MultiIndex', 'IntervalIndex', 'DatetimeIndex', 'TimedeltaIndex', 'PeriodIndex', 'Int64Index', 'UInt64Index', 'Float64Index'
            // GroupBy 하위 유형
            , 'DataFrameGroupBy', 'SeriesGroupBy'
            // Plot 관련 유형
            , 'Figure', 'AxesSubplot'
            // Numpy
            , 'ndarray'
            // Python 변수
            , 'str', 'int', 'float', 'bool', 'dict', 'list', 'tuple'
        ];
        /**
         * 변수 조회 시 제외해야할 변수명
         */
        var _VP_NOT_USING_VAR = ['_html', '_nms', 'NamespaceMagics', '_Jupyter', 'In', 'Out', 'exit', 'quit', 'get_ipython'];
        /**
         * 변수 조회 시 제외해야할 변수 타입
         */
        var _VP_NOT_USING_TYPE = ['module', 'function', 'builtin_function_or_method', 'instance', '_Feature', 'type', 'ufunc'];

        // types에 맞는 변수목록 조회하는 명령문 구성
        var cmdSB = new sb.StringBuilder();
        cmdSB.append(`print([{'varName': v, 'varType': type(eval(v)).__name__}`);
        cmdSB.appendFormat(`for v in dir() if (v not in {0}) `, JSON.stringify(_VP_NOT_USING_VAR));
        cmdSB.appendFormat(`& (type(eval(v)).__name__ not in {0}) `, JSON.stringify(_VP_NOT_USING_TYPE));
        cmdSB.appendFormat(`& (type(eval(v)).__name__ in {0})])`, JSON.stringify(types));

        // FIXME: vpFuncJS에만 kernel 사용하는 메서드가 정의되어 있어서 임시로 사용
        vp_executePython(cmdSB.toString(), function(result) {
            // callback(result);
            blockContainer.setKernelLoadedVariableList(result);
        });
    }

    /**
     * FIXME: vpFuncJS에만 kernel 사용하는 메서드가 정의되어 있어서 임시로 사용
     * @param {*} command 
     * @param {*} callback 
     * @param {*} isSilent 
     */
    var vp_executePython = function (command, callback, isSilent = false) {
        Jupyter.notebook.kernel.execute(
            command,
            {
                iopub: {
                    output: function (msg) {
                        var result = String(msg.content["text"]);
                        /** parsing */
                        var jsonVars = result.replace(/'/gi, `"`);
                        var varList = JSON.parse(jsonVars);

                        /** '_' 가 들어간 변수목록 제거 */
                        var filteredVarlist = varList.filter(varData => {
                            if (varData.varName.indexOf('_') != -1) {
                                return false;
                            } else {
                                return true;
                            }
                        });
                        callback(filteredVarlist);
                    }
                }
            },
            { silent: isSilent }
        );
    };
    return {
        ControlToggleInput

        , CreateOneArrayValueAndGet
        , UpdateOneArrayValueAndGet
        , DeleteOneArrayValueAndGet

        , SetChildBlockList_down_first_indent_last

        , MapGroupTypeToName
        , MapTypeToName
        , RemoveSomeBlockAndGetBlockList
        
        , MapNewLineStrToIndentString
        
        , SetTextareaLineNumber_apiBlock

        , IsCanHaveIndentBlock
        , IsCodeBlockType
        , IsElifElseExceptFinallyBlockType
        , IsIfForTryBlockType
        , IsNodeTextBlockType
        , IsDefineBlockType
        , IsControlBlockType

        , LoadVariableList

        , RenderInputRequiredColor
        , RenderSelectRequiredColor
     
        , RenderCodeBlockInputRequired
        
        , RenderHTMLDomColor
 
        , GenerateClassInParamList
        , GenerateDefInParamList
        , GenerateReturnOutParamList
        , GenerateIfConditionList
        , GenerateExceptConditionList
        , GenerateForParam
        , GenerateListforConditionList
        , GenerateLambdaParamList
        , GenerateImportList
        , GenerateWhileBlockCode
        , GenerateWhileConditionList

        , ShowImportListAtBlock
        , ShowCodeBlockCode
    }
});
