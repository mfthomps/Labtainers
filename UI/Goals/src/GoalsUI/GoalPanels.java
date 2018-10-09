/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package GoalsUI;

import static GoalsUI.ParamReferenceStorage.GoalType_ITEMS;
import static GoalsUI.ParamReferenceStorage.Operator_ITEMS;
import static GoalsUI.ParamReferenceStorage.answerTypes;
import static GoalsUI.ParamReferenceStorage.goalInput;
import static GoalsUI.ParamReferenceStorage.opInput;
import static GoalsUI.ParamReferenceStorage.resultTagInput;
import GoalsUI.ToolTipHandlers.ToolTipWrapper;
import static GoalsUI.ToolTipHandlers.setComboItems;
import java.awt.Dimension;
import java.util.List;
import javax.swing.DefaultComboBoxModel;
import javax.swing.JComboBox;
import javax.swing.JPanel;
import javax.swing.JTextField;

/**
 *
 * @author Dan
 */

//NOTE: Previous Matchany ComboBox has not been implemented at all- 9/13/17



public class GoalPanels extends javax.swing.JPanel {
    static Dimension dim = new Dimension(975, 100);
    private GoalsUI goalsUI;
    private int rowNum;
    
    private List<String> resultTags;
    private List<String> parameterIDs;
    private List<String> booleanResultTags;
        
    //Creating fresh goal line
    public GoalPanels(GoalsUI ui, GoalsData dataUI) {
        initiateGoalPanel(ui, dataUI, dataUI.getRowCount());    
        this.revalidate();
        this.repaint();
    }
   
    //Loading goal line
    public GoalPanels(GoalsUI ui, GoalsData dataUI, GoalValues goalVal, int rowNum) {
        initiateGoalPanel(ui, dataUI, rowNum);
        
        //Set Values
        setGoalIDTextField(goalVal.goalID);
 
        setGoalTypeComboBox(goalVal.goalType);
 
        setOperatorComboBox(goalVal.operator);
  
        setExecutableFileTextField(goalVal.executableFile);

        setResultTagComboBox(goalVal.resultTag);

        setArithmeticResultTagTextField(goalVal.resultTag);

        setAnswerTypeComboBox(goalVal.answerType);
        
        if(goalVal.answerType.equals(answerTypes[0])) //Literal
            setAnswerTagTextField(goalVal.answerTag);
        else if(goalVal.answerType.equals(answerTypes[1])) //Result Tag
            setResultTag2ComboBox(goalVal.answerTag);
        else //Parameter & Parameter_ASCII
            setParameterComboBox(goalVal.answerTag);
        
        setBooleanTextField(goalVal.booleanExp);

        setGoal1TextField(goalVal.goal1);

        setGoal2TextField(goalVal.goal2);

        setValueTextField(goalVal.value);
 
        setSubgoalTextField(goalVal.subgoalList);

        this.revalidate();
        this.repaint();
        
    }
    
    //Use for loading a line
    private void initiateGoalPanel(GoalsUI ui, GoalsData dataUI, int rowNum){
        initComponents();
        this.goalsUI = ui;
        this.rowNum = rowNum;
        
        resultTags = dataUI.getResultTagList();
        parameterIDs = dataUI.getParameters();
        booleanResultTags = dataUI.getBooleanResults();
                
        rowLabel.setText(Integer.toString(rowNum));
        
        //Set initial field visibility. Defaults to [operator : resultTag : answerTag]
        AnswerTagTextField.setVisible(true);
        ResultTag2ComboBox.setVisible(false);
        ParameterComboBox.setVisible(false);
        ArithmeticResultTagTextField.setVisible(false);
        BooleanTextField.setVisible(false);
        ExecutableFileTextField.setVisible(false);
        Goal1TextField.setVisible(false);
        Goal2TextField.setVisible(false);
        ResultTagComboBox.setVisible(false);
        SubgoalTextField.setVisible(false);
        ValueTextField.setVisible(false);
        BooleanResultTagsComboBox.setVisible(false);
        PreviousMatchanyComboBox.setVisible(false);
        
        
        //Load ComboBox Items       
        setComboItems(GoalTypeComboBox, GoalType_ITEMS);
        setComboItems(OperatorComboBox, Operator_ITEMS);
        
            
        
        ResultTagComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(resultTags.toArray(new String[resultTags.size()])));
        AnswerTypeComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(answerTypes)); 
        if(parameterIDs.isEmpty()){
            AnswerTypeComboBox.removeItem(answerTypes[2]);
            AnswerTypeComboBox.removeItem(answerTypes[3]);            
        }
        else
            ParameterComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(parameterIDs.toArray(new String[parameterIDs.size()])));
           
        ResultTag2ComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(resultTags.toArray(new String[resultTags.size()])));
        BooleanResultTagsComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(booleanResultTags.toArray(new String[booleanResultTags.size()])));
    }
    
    
    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        ArtifactPanel = new javax.swing.JPanel();
        GoalIDTextField = new javax.swing.JTextField();
        GoalTypeComboBox = new javax.swing.JComboBox<>();
        OperatorComboBox = new javax.swing.JComboBox<>();
        AnswerTagTextField = new javax.swing.JTextField();
        BooleanTextField = new javax.swing.JTextField();
        Goal1TextField = new javax.swing.JTextField();
        Goal2TextField = new javax.swing.JTextField();
        ValueTextField = new javax.swing.JTextField();
        SubgoalTextField = new javax.swing.JTextField();
        ResultTagComboBox = new javax.swing.JComboBox<>();
        ExecutableFileTextField = new javax.swing.JTextField();
        ArithmeticResultTagTextField = new javax.swing.JTextField();
        AnswerTypeComboBox = new javax.swing.JComboBox<>();
        ResultTag2ComboBox = new javax.swing.JComboBox<>();
        ParameterComboBox = new javax.swing.JComboBox<>();
        BooleanResultTagsComboBox = new javax.swing.JComboBox<>();
        PreviousMatchanyComboBox = new javax.swing.JComboBox<>();
        DeleteButton = new javax.swing.JButton();
        rowLabel = new javax.swing.JLabel();
        UpButton = new javax.swing.JButton();
        DownButton = new javax.swing.JButton();

        setPreferredSize(new java.awt.Dimension(1110, 69));

        ArtifactPanel.setBorder(new javax.swing.border.SoftBevelBorder(javax.swing.border.BevelBorder.RAISED));
        ArtifactPanel.setMinimumSize(new java.awt.Dimension(1400, 0));
        ArtifactPanel.setPreferredSize(new java.awt.Dimension(1300, 34));

        GoalTypeComboBox.addItemListener(new java.awt.event.ItemListener() {
            public void itemStateChanged(java.awt.event.ItemEvent evt) {
                goalTypeItemChanged(evt);
            }
        });

        OperatorComboBox.setToolTipText("Identifies how the line is to be identified");
        OperatorComboBox.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createEtchedBorder(), "Operator"));

        AnswerTagTextField.setToolTipText("Parameter based on Line Type");
        AnswerTagTextField.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createEtchedBorder(), "AnswerTag"));

        BooleanTextField.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createEtchedBorder(), "Boolean"));

        Goal1TextField.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createEtchedBorder(), "Goal 1"));

        Goal2TextField.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createEtchedBorder(), "Goal 2"));

        ValueTextField.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createEtchedBorder(), "Value"));

        SubgoalTextField.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createEtchedBorder(), "Subgoal List"));

        ResultTagComboBox.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createEtchedBorder(), "Result Tag"));

        ExecutableFileTextField.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createEtchedBorder(), "Executable File"));

        ArithmeticResultTagTextField.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createEtchedBorder(), "Arithmetic Result Tag"));

        AnswerTypeComboBox.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createEtchedBorder(), "Answer Type"));
        AnswerTypeComboBox.addItemListener(new java.awt.event.ItemListener() {
            public void itemStateChanged(java.awt.event.ItemEvent evt) {
                AnswerTypeComboBoxItemStateChanged(evt);
            }
        });

        BooleanResultTagsComboBox.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createEtchedBorder(), "Boolean Result Tags"));

        javax.swing.GroupLayout ArtifactPanelLayout = new javax.swing.GroupLayout(ArtifactPanel);
        ArtifactPanel.setLayout(ArtifactPanelLayout);
        ArtifactPanelLayout.setHorizontalGroup(
            ArtifactPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(ArtifactPanelLayout.createSequentialGroup()
                .addContainerGap()
                .addComponent(GoalIDTextField, javax.swing.GroupLayout.PREFERRED_SIZE, 125, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(GoalTypeComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, 147, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(OperatorComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, 139, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(ExecutableFileTextField, javax.swing.GroupLayout.PREFERRED_SIZE, 143, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(ResultTagComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, 168, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(2, 2, 2)
                .addComponent(ArithmeticResultTagTextField, javax.swing.GroupLayout.PREFERRED_SIZE, 179, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(AnswerTypeComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, 150, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(AnswerTagTextField, javax.swing.GroupLayout.PREFERRED_SIZE, 193, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(ResultTag2ComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, 155, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(ParameterComboBox, 0, 150, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(BooleanTextField, javax.swing.GroupLayout.PREFERRED_SIZE, 404, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(ValueTextField, javax.swing.GroupLayout.PREFERRED_SIZE, 110, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(SubgoalTextField, javax.swing.GroupLayout.PREFERRED_SIZE, 643, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(Goal1TextField, javax.swing.GroupLayout.PREFERRED_SIZE, 185, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(Goal2TextField, javax.swing.GroupLayout.PREFERRED_SIZE, 126, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(BooleanResultTagsComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, 162, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(PreviousMatchanyComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        ArtifactPanelLayout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {Goal1TextField, Goal2TextField});

        ArtifactPanelLayout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {ParameterComboBox, ResultTag2ComboBox});

        ArtifactPanelLayout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {BooleanResultTagsComboBox, PreviousMatchanyComboBox});

        ArtifactPanelLayout.setVerticalGroup(
            ArtifactPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, ArtifactPanelLayout.createSequentialGroup()
                .addGap(14, 14, 14)
                .addGroup(ArtifactPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING, false)
                    .addGroup(ArtifactPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                        .addGroup(ArtifactPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(ValueTextField, javax.swing.GroupLayout.PREFERRED_SIZE, 44, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(SubgoalTextField, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addComponent(Goal2TextField, javax.swing.GroupLayout.Alignment.TRAILING)
                        .addGroup(ArtifactPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(GoalIDTextField, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(GoalTypeComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addGroup(ArtifactPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(BooleanTextField, javax.swing.GroupLayout.PREFERRED_SIZE, 41, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(Goal1TextField, javax.swing.GroupLayout.PREFERRED_SIZE, 41, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addGroup(ArtifactPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(OperatorComboBox)
                            .addComponent(ExecutableFileTextField, javax.swing.GroupLayout.PREFERRED_SIZE, 44, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(ResultTagComboBox)
                            .addComponent(ArithmeticResultTagTextField)
                            .addComponent(AnswerTypeComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(AnswerTagTextField, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addComponent(ResultTag2ComboBox, javax.swing.GroupLayout.Alignment.TRAILING)
                        .addComponent(ParameterComboBox, javax.swing.GroupLayout.Alignment.TRAILING))
                    .addComponent(BooleanResultTagsComboBox)
                    .addComponent(PreviousMatchanyComboBox))
                .addGap(83, 83, 83))
        );

        ArtifactPanelLayout.linkSize(javax.swing.SwingConstants.VERTICAL, new java.awt.Component[] {Goal1TextField, Goal2TextField, SubgoalTextField, ValueTextField});

        ArtifactPanelLayout.linkSize(javax.swing.SwingConstants.VERTICAL, new java.awt.Component[] {AnswerTagTextField, AnswerTypeComboBox, ArithmeticResultTagTextField, BooleanTextField, ExecutableFileTextField, OperatorComboBox, ParameterComboBox, ResultTag2ComboBox, ResultTagComboBox});

        DeleteButton.setText("Delete");
        DeleteButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                DeleteButtonActionPerformed(evt);
            }
        });

        rowLabel.setFont(new java.awt.Font("Arial", 1, 24)); // NOI18N
        rowLabel.setText("10");

        UpButton.setText("^");
        UpButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                UpButtonActionPerformed(evt);
            }
        });

        DownButton.setText("v");
        DownButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                DownButtonActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(rowLabel)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addComponent(ArtifactPanel, javax.swing.GroupLayout.PREFERRED_SIZE, 1390, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                    .addComponent(UpButton, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(DownButton, javax.swing.GroupLayout.PREFERRED_SIZE, 41, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(DeleteButton)
                .addGap(73, 73, 73))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(ArtifactPanel, javax.swing.GroupLayout.PREFERRED_SIZE, 80, javax.swing.GroupLayout.PREFERRED_SIZE)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                        .addGroup(layout.createSequentialGroup()
                            .addComponent(UpButton)
                            .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                            .addComponent(DownButton))
                        .addComponent(DeleteButton, javax.swing.GroupLayout.PREFERRED_SIZE, 58, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addComponent(rowLabel)))
        );
    }// </editor-fold>//GEN-END:initComponents

    private void DeleteButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_DeleteButtonActionPerformed
       deleteButton();
    }//GEN-LAST:event_DeleteButtonActionPerformed

    private void deleteButton(){
       JPanel container = (JPanel)this.getParent();
       container.remove(this);
       goalsUI.dataUI.decreaseRowCount();
       goalsUI.refresh();
    }
    
    private void UpButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_UpButtonActionPerformed
        swapUpdate("UP", rowNum-1); //Subtract rowNum by one to get the proper index number
    }//GEN-LAST:event_UpButtonActionPerformed

    private void DownButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_DownButtonActionPerformed
        swapUpdate("DOWN", rowNum-1); //Subtract rowNum by one to get the proper index number
    }//GEN-LAST:event_DownButtonActionPerformed

    private void goalTypeItemChanged(java.awt.event.ItemEvent evt) {//GEN-FIRST:event_goalTypeItemChanged
        goalTypeListener();
    }//GEN-LAST:event_goalTypeItemChanged

    private void AnswerTypeComboBoxItemStateChanged(java.awt.event.ItemEvent evt) {//GEN-FIRST:event_AnswerTypeComboBoxItemStateChanged
        answerTypeListener();
    }//GEN-LAST:event_AnswerTypeComboBoxItemStateChanged

    private void goalTypeListener(){
        String goalType = ((ToolTipWrapper)GoalTypeComboBox.getSelectedItem()).getItem();
        
        if(opInput.contains(goalType))
            visibilityHandler("op");
        else if(goalInput.contains(goalType))
            visibilityHandler("goal");
        else if(resultTagInput.contains(goalType)) 
            visibilityHandler("rT");
        else if("boolean".equals(goalType))
           visibilityHandler("boolean");
        else if("count_greater".equals(goalType))
            visibilityHandler("countg");
        else if("execute".equals(goalType))
           visibilityHandler("exe");
        else if("matchExpression".equals(goalType))
            visibilityHandler("matche");    
        else
            System.out.println("Goal Type Listener could not find this type: " + goalType);
    }
    
    private void visibilityHandler(String type){
        OperatorComboBox.setVisible(false);
        if(((DefaultComboBoxModel)OperatorComboBox.getModel()).getIndexOf(Operator_ITEMS[4]) == -1) 
           OperatorComboBox.insertItemAt(Operator_ITEMS[4], 0);
        if(((DefaultComboBoxModel)OperatorComboBox.getModel()).getIndexOf(Operator_ITEMS[2]) == -1) 
           OperatorComboBox.insertItemAt(Operator_ITEMS[3], 0);
        if(((DefaultComboBoxModel)OperatorComboBox.getModel()).getIndexOf(Operator_ITEMS[2]) == -1) 
           OperatorComboBox.insertItemAt(Operator_ITEMS[2], 0);
        if(((DefaultComboBoxModel)OperatorComboBox.getModel()).getIndexOf(Operator_ITEMS[1]) == -1) 
           OperatorComboBox.insertItemAt(Operator_ITEMS[1], 0);
        if(((DefaultComboBoxModel)OperatorComboBox.getModel()).getIndexOf(Operator_ITEMS[0]) == -1) 
           OperatorComboBox.insertItemAt(Operator_ITEMS[0], 0);
        
        OperatorComboBox.setSelectedItem(Operator_ITEMS[0]);
        
        
        
        ExecutableFileTextField.setVisible(false);
        ExecutableFileTextField.setText("");

        ResultTagComboBox.setVisible(false);
        if(resultTags != null && !resultTags.isEmpty())
            ResultTagComboBox.setSelectedItem(resultTags.get(0)); 
        
        ArithmeticResultTagTextField.setVisible(false);
        ArithmeticResultTagTextField.setText("");
        
        AnswerTypeComboBox.setVisible(false);
        AnswerTypeComboBox.setSelectedItem(answerTypes[0]);
        //"Result Tag" may have been removed by the execute goaltype so readd it to the combo box to reset it back to default
        if(((DefaultComboBoxModel)AnswerTypeComboBox.getModel()).getIndexOf("Result Tag") == -1) 
            AnswerTypeComboBox.addItem("Result Tag");
        AnswerTagTextField.setVisible(false);
        AnswerTagTextField.setText("");
         
        ResultTag2ComboBox.setVisible(false);
        if(resultTags != null && !resultTags.isEmpty())
            ResultTag2ComboBox.setSelectedItem(resultTags.get(0));
            
        ParameterComboBox.setVisible(false);
        if(parameterIDs != null && !parameterIDs.isEmpty())
                ParameterComboBox.setSelectedItem(parameterIDs.get(0));

        BooleanTextField.setVisible(false);
        BooleanTextField.setText("");

        Goal1TextField.setVisible(false);
        Goal1TextField.setText("");

        Goal2TextField.setVisible(false);
        Goal2TextField.setText("");

        SubgoalTextField.setVisible(false);
        SubgoalTextField.setText("");

        ValueTextField.setVisible(false);
        ValueTextField.setText("");

        BooleanResultTagsComboBox.setVisible(false);
        if(booleanResultTags != null && !booleanResultTags.isEmpty())
            BooleanResultTagsComboBox.setSelectedItem(booleanResultTags.get(0));

        PreviousMatchanyComboBox.setVisible(false);
        //if(prevMatchany != null && !prevMatchany.isEmpty())
        //    PreviousMatchanyComboBox.setSelectedItem(prevMatchany.get(0));
    
        switch(type){
            case "op":
                OperatorComboBox.setVisible(true);
                ResultTagComboBox.setVisible(true);
                AnswerTypeComboBox.setVisible(true);
                AnswerTagTextField.setVisible(true);
                break;
            case "goal":
                Goal1TextField.setVisible(true);
                Goal2TextField.setVisible(true);
                BooleanResultTagsComboBox.setVisible(true);
                //PreviousMatchanyComboBox.setVisible(true);
                break;
            case "rT":
                ResultTagComboBox.setVisible(true);
                break;
            case "boolean":
                BooleanTextField.setVisible(true);
                BooleanResultTagsComboBox.setVisible(true);
                break;
            case "countg":
                SubgoalTextField.setVisible(true);
                ValueTextField.setVisible(true);
                BooleanResultTagsComboBox.setVisible(true);
                break;
            case "exe":
                ExecutableFileTextField.setVisible(true);
                ResultTagComboBox.setVisible(true);
                AnswerTypeComboBox.setVisible(true);
                //Answertag is expected to be a literal value or a symbolic name from parameters.config (pg. 26 in labtainers manual)
                AnswerTypeComboBox.removeItem("Result Tag");
                AnswerTagTextField.setVisible(true);
                break;
            case "matche":
                OperatorComboBox.setVisible(true);
                OperatorComboBox.removeItem(Operator_ITEMS[0]);
                OperatorComboBox.removeItem(Operator_ITEMS[1]);
                OperatorComboBox.removeItem(Operator_ITEMS[2]);
                OperatorComboBox.removeItem(Operator_ITEMS[3]);
                OperatorComboBox.removeItem(Operator_ITEMS[4]);
                ArithmeticResultTagTextField.setVisible(true);
                AnswerTypeComboBox.setVisible(true);  
                AnswerTagTextField.setVisible(true);
                break;
            default:
                System.out.println("No type match");
        }
            
        this.revalidate();
        this.repaint();
    }
        
    private void answerTypeListener(){
        String answerType = (String)(AnswerTypeComboBox.getSelectedItem());
        
        if(answerType.equals(answerTypes[0])){ //Literal
            AnswerTagTextField.setVisible(true);
            
            ResultTag2ComboBox.setVisible(false);
            if(resultTags != null && !resultTags.isEmpty())
                ResultTag2ComboBox.setSelectedItem(resultTags.get(0));
            
            ParameterComboBox.setVisible(false);
            if(parameterIDs != null && !parameterIDs.isEmpty())
                ParameterComboBox.setSelectedItem(parameterIDs.get(0));
        }
        else if(answerType.equals(answerTypes[1])){ //Result Tag
            AnswerTagTextField.setVisible(false);
            AnswerTagTextField.setText("");
            
            ResultTag2ComboBox.setVisible(true);
            
            ParameterComboBox.setVisible(false);
            if(parameterIDs != null && !parameterIDs.isEmpty())
                ParameterComboBox.setSelectedItem(parameterIDs.get(0));
        }
        else if(answerType.equals(answerTypes[2]) || answerType.equals(answerTypes[3])){
            AnswerTagTextField.setVisible(false);
            AnswerTagTextField.setText("");
            
            ResultTag2ComboBox.setVisible(false);
            if(resultTags != null && !resultTags.isEmpty())
                ResultTag2ComboBox.setSelectedItem(resultTags.get(0));
            
            ParameterComboBox.setVisible(true);
        }
        
        this.revalidate();
        this.repaint();
    }
    
    //Swaps goal order in the list of goals and then redraws them
    protected void swapUpdate(String type, int rowIndex){
        goalsUI.dataUI.updateListofGoals(goalsUI.getPanelofGoals());
        goalsUI.dataUI.swapGoals(type, rowIndex);
        goalsUI.goalsPanelRedraw();
    }
   

    //Field Getters
    public JTextField getGoalIDTextField(){
        return GoalIDTextField;
    }
    
    public JComboBox<ToolTipWrapper> getGoalTypeComboBox(){
        return GoalTypeComboBox;
    }
    
    public JComboBox<ToolTipWrapper> getOperatorComboBox(){
        return OperatorComboBox;
    }
    
    public JTextField getExecutableFileTextField(){
        return ExecutableFileTextField;
    }
    
    public JComboBox<String> getResultTagComboBox(){
        return ResultTagComboBox;
    }
    
    public JTextField getArithmeticResultTagTextField(){
        return ArithmeticResultTagTextField;
    }
    
    public JComboBox getAnswerTypeComboBox(){
        return AnswerTypeComboBox;
    }
    
    public JTextField getAnswerTagTextField(){
        return AnswerTagTextField;
    }
    
    public JComboBox getResultTag2ComboBox(){
        return ResultTag2ComboBox;
    }
    
    public JComboBox getParameterComboBox(){
        return ParameterComboBox;
    }
      
    public JTextField getBooleanTextField(){
        return BooleanTextField;
    }
    
    public JTextField getGoal1TextField(){
        return Goal1TextField;
    }
    
    public JTextField getGoal2TextField(){
        return Goal2TextField;
    }
    
    public JTextField getValueTextField(){
        return ValueTextField;
    }
    
    public JTextField getSubgoalTextField(){
        return SubgoalTextField;
    }
    
    
  
    //Field SETTERS
    private void setGoalIDTextField(String v){
        GoalIDTextField.setText(v);
    }
    
    private void setGoalTypeComboBox(ToolTipWrapper v){
        GoalTypeComboBox.setSelectedItem(v);
    }
    
    private void setOperatorComboBox(ToolTipWrapper v){
        OperatorComboBox.setSelectedItem(v);
    }
    
    private void setExecutableFileTextField(String v){
        ExecutableFileTextField.setText(v);
    }
    
    private void setResultTagComboBox(String v){
        ResultTagComboBox.setSelectedItem(v);
    }
    
    private void setArithmeticResultTagTextField(String v){
        ArithmeticResultTagTextField.setText(v);
    }
    
    private void setAnswerTypeComboBox(String v){
        AnswerTypeComboBox.setSelectedItem(v);
    }
    
    private void setAnswerTagTextField(String v){
        AnswerTagTextField.setText(v);
    }
    
    private void setResultTag2ComboBox(String v){
        ResultTag2ComboBox.setSelectedItem(v);
    }
    
    private void setParameterComboBox(String v){
        ParameterComboBox.setSelectedItem(v);
    }
    
    private void setBooleanTextField(String v){
        BooleanTextField.setText(v);
    }
    
    private void setGoal1TextField(String v){
        Goal1TextField.setText(v);
    }
    
    private void setGoal2TextField(String v){
        Goal2TextField.setText(v);
    }
    
    private void setValueTextField(String v){
        ValueTextField.setText(v);
    }
    
    private void setSubgoalTextField(String v){
        SubgoalTextField.setText(v);
    }
    

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JTextField AnswerTagTextField;
    private javax.swing.JComboBox<String> AnswerTypeComboBox;
    private javax.swing.JTextField ArithmeticResultTagTextField;
    private javax.swing.JPanel ArtifactPanel;
    private javax.swing.JComboBox<String> BooleanResultTagsComboBox;
    private javax.swing.JTextField BooleanTextField;
    private javax.swing.JButton DeleteButton;
    private javax.swing.JButton DownButton;
    private javax.swing.JTextField ExecutableFileTextField;
    private javax.swing.JTextField Goal1TextField;
    private javax.swing.JTextField Goal2TextField;
    private javax.swing.JTextField GoalIDTextField;
    private javax.swing.JComboBox<ToolTipWrapper> GoalTypeComboBox;
    private javax.swing.JComboBox<ToolTipWrapper> OperatorComboBox;
    private javax.swing.JComboBox<String> ParameterComboBox;
    private javax.swing.JComboBox<String> PreviousMatchanyComboBox;
    private javax.swing.JComboBox<String> ResultTag2ComboBox;
    private javax.swing.JComboBox<String> ResultTagComboBox;
    private javax.swing.JTextField SubgoalTextField;
    private javax.swing.JButton UpButton;
    private javax.swing.JTextField ValueTextField;
    private javax.swing.JLabel rowLabel;
    // End of variables declaration//GEN-END:variables
}
