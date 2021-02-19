/*
This software was created by United States Government employees at 
The Center for Cybersecurity and Cyber Operations (C3O) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
 */
package labtainers.goalsui;

import java.awt.Dimension;
import java.util.List;
import javax.swing.DefaultComboBoxModel;
import javax.swing.JComboBox;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.JDialog;
import static labtainers.goalsui.ParamReferenceStorage.GoalType_ITEMS;
import static labtainers.goalsui.ParamReferenceStorage.Operator_ITEMS;
import static labtainers.goalsui.ParamReferenceStorage.Answer_ITEMS;
import static labtainers.goalsui.ParamReferenceStorage.goalInput;
import static labtainers.goalsui.ParamReferenceStorage.opInput;
import static labtainers.goalsui.ParamReferenceStorage.resultTagInput;
import labtainers.goalsui.ParamReferenceStorage;
import labtainers.mainui.ToolTipHandlers.ToolTipWrapper;
import static labtainers.mainui.ToolTipHandlers.setComboItems;

/**
 *
 * @author student
 */
public class GoalPanels extends javax.swing.JPanel {

    /**
     * Creates new form GoalPanels
     */
    static Dimension dim = new Dimension(975, 100);
    private GoalsUI goalsUI;
    private GoalsData dataUI;
    private int rowNum;
    
    private List<String> resultTags;
    private List<String> parameterIDs;
    private List<String> booleanResultTags;
    private String comments;
     
    //Creating fresh goal line
    public GoalPanels(GoalsUI ui, GoalsData dataUI) {
        initiateGoalPanel(ui, dataUI, dataUI.getRowCount());    
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
         
        if(goalVal.answerType.equals(Answer_ITEMS[0].getItem())){
             //Literal
            //System.out.println("literal set "+goalVal.answerTag);
            setAnswerTagTextField(goalVal.answerTag);
        }else if(goalVal.answerType.equals(Answer_ITEMS[1].getItem())){
            //Result Tag
            setResultTag2ComboBox(goalVal.answerTag);
        }else{
            //Parameter & Parameter_ASCII
            setParameterComboBox(goalVal.answerTag);
        }
        
        setBooleanTextField(goalVal.booleanExp);

        setGoal1TextField(goalVal.goal1);

        setGoal2TextField(goalVal.goal2);

        setValueTextField(goalVal.value);
 
        setSubgoalTextField(goalVal.subgoalList);

        this.comments = goalVal.comments;

        this.revalidate();
        this.repaint();
        
    }
    
     //Use for loading a line
    private void initiateGoalPanel(GoalsUI ui, GoalsData dataUI, int rowNum){
        initComponents();
        this.goalsUI = ui;
        this.dataUI = dataUI;
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
        AnswerTypeComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(Answer_ITEMS)); 
        if(parameterIDs.isEmpty()){
            AnswerTypeComboBox.removeItem(Answer_ITEMS[2]);
            AnswerTypeComboBox.removeItem(Answer_ITEMS[3]);            
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
        DocButton = new javax.swing.JButton();

        setMinimumSize(new java.awt.Dimension(1110, 69));

        ArtifactPanel.setBorder(new javax.swing.border.SoftBevelBorder(javax.swing.border.BevelBorder.RAISED));
        ArtifactPanel.setMinimumSize(new java.awt.Dimension(1400, 0));
        ArtifactPanel.setPreferredSize(new java.awt.Dimension(1300, 34));

        GoalTypeComboBox.setToolTipText("Hover over pulldown items for information about each goal type.");
        GoalTypeComboBox.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createEtchedBorder(), "Goal Type"));
        GoalTypeComboBox.addItemListener(new java.awt.event.ItemListener() {
            public void itemStateChanged(java.awt.event.ItemEvent evt) {
                GoalTypeComboBoxgoalTypeItemChanged(evt);
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

        AnswerTypeComboBox.setToolTipText("Hover over pulldown values for information about different answer types.");
        AnswerTypeComboBox.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createEtchedBorder(), "Answer Type"));
        AnswerTypeComboBox.addItemListener(new java.awt.event.ItemListener() {
            public void itemStateChanged(java.awt.event.ItemEvent evt) {
                AnswerTypeComboBoxItemStateChanged(evt);
            }
        });

        ParameterComboBox.setToolTipText("Parameter whose value is to be compared.");
        ParameterComboBox.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createEtchedBorder(), "Parameter"));

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
                .addGap(52, 52, 52)
                .addComponent(ResultTag2ComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, 155, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(ParameterComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, 153, javax.swing.GroupLayout.PREFERRED_SIZE)
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
        ArtifactPanelLayout.setVerticalGroup(
            ArtifactPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(ArtifactPanelLayout.createSequentialGroup()
                .addGap(14, 14, 14)
                .addGroup(ArtifactPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(ArtifactPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                        .addComponent(GoalTypeComboBox, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(OperatorComboBox, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addGroup(ArtifactPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                        .addComponent(ParameterComboBox)
                        .addGroup(ArtifactPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(ValueTextField, javax.swing.GroupLayout.PREFERRED_SIZE, 44, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(SubgoalTextField, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addComponent(Goal2TextField, javax.swing.GroupLayout.Alignment.TRAILING)
                        .addGroup(ArtifactPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(BooleanTextField, javax.swing.GroupLayout.PREFERRED_SIZE, 41, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(Goal1TextField, javax.swing.GroupLayout.PREFERRED_SIZE, 41, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addGroup(ArtifactPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(ExecutableFileTextField, javax.swing.GroupLayout.PREFERRED_SIZE, 44, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(ResultTagComboBox)
                            .addComponent(ArithmeticResultTagTextField)
                            .addComponent(AnswerTypeComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(AnswerTagTextField, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addComponent(ResultTag2ComboBox, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(BooleanResultTagsComboBox, javax.swing.GroupLayout.Alignment.TRAILING)
                        .addComponent(PreviousMatchanyComboBox, javax.swing.GroupLayout.Alignment.TRAILING)
                        .addComponent(GoalIDTextField, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

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

        DocButton.setText("Doc");
        DocButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                DocButtonActionPerformed(evt);
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
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(DocButton)
                    .addComponent(DeleteButton))
                .addGap(51, 51, 51))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(UpButton)
                            .addComponent(DeleteButton, javax.swing.GroupLayout.PREFERRED_SIZE, 30, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(DownButton)
                            .addComponent(DocButton)))
                    .addComponent(rowLabel))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
            .addComponent(ArtifactPanel, javax.swing.GroupLayout.DEFAULT_SIZE, 92, Short.MAX_VALUE)
        );
    }// </editor-fold>//GEN-END:initComponents

    private void GoalTypeComboBoxgoalTypeItemChanged(java.awt.event.ItemEvent evt) {//GEN-FIRST:event_GoalTypeComboBoxgoalTypeItemChanged
        goalTypeListener();
    }//GEN-LAST:event_GoalTypeComboBoxgoalTypeItemChanged

    private void AnswerTypeComboBoxItemStateChanged(java.awt.event.ItemEvent evt) {//GEN-FIRST:event_AnswerTypeComboBoxItemStateChanged
        answerTypeListener();
    }//GEN-LAST:event_AnswerTypeComboBoxItemStateChanged

    private void DeleteButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_DeleteButtonActionPerformed
        deleteButton();
    }//GEN-LAST:event_DeleteButtonActionPerformed

    private void UpButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_UpButtonActionPerformed
        swapUpdate("UP", rowNum-1); //Subtract rowNum by one to get the proper index number
    }//GEN-LAST:event_UpButtonActionPerformed

    private void DownButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_DownButtonActionPerformed
        swapUpdate("DOWN", rowNum-1); //Subtract rowNum by one to get the proper index number
    }//GEN-LAST:event_DownButtonActionPerformed

    private void DocButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_DocButtonActionPerformed
        DocPanel panel = new DocPanel();

        panel.setDoc(this.comments);
        //panel.setVisible(true);
        JDialog dialog = new JDialog();
        panel.setDialog(dialog);
        //dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        dialog.setModal(true);
        dialog.add(panel);
        dialog.pack();
        dialog.setLocation(200, 200);
        dialog.setTitle("Documentation for "+GoalIDTextField.getText());
        dialog.setVisible(true);
        if(panel.isOK()){
            this.comments = panel.getDoc();
        }
        dialog.dispose();

    }//GEN-LAST:event_DocButtonActionPerformed

    // BUTTONS and LISTENERS //
    
    private void deleteButton(){
       JPanel container = (JPanel)this.getParent();
       container.remove(this);
       goalsUI.data.decreaseRowCount();
       goalsUI.refresh();
    }
    
    private void goalTypeListener(){
        Object item = GoalTypeComboBox.getSelectedItem();
        if(item == null){
           System.out.println("Goal type item "+item);
           return; 
        }
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
        if(((DefaultComboBoxModel)OperatorComboBox.getModel()).getIndexOf(Operator_ITEMS[5]) == -1) 
           OperatorComboBox.insertItemAt(Operator_ITEMS[5], 0);
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
        AnswerTypeComboBox.setSelectedItem(Answer_ITEMS[0]);
        //"Result Tag" may have been removed by the execute goaltype so readd it to the combo box to reset it back to default
        if(((DefaultComboBoxModel)AnswerTypeComboBox.getModel()).getIndexOf("Result Tag") == -1) 
            AnswerTypeComboBox.addItem(Answer_ITEMS[1]);
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
                AnswerTypeComboBox.removeItem(Answer_ITEMS[1]); // Result Tag
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
        ToolTipWrapper answerType = (ToolTipWrapper)(AnswerTypeComboBox.getSelectedItem());
        
        if(answerType.equals(Answer_ITEMS[0])){ //Literal
            AnswerTagTextField.setVisible(true);
            
            ResultTag2ComboBox.setVisible(false);
            if(resultTags != null && !resultTags.isEmpty())
                ResultTag2ComboBox.setSelectedItem(resultTags.get(0));
            
            ParameterComboBox.setVisible(false);
            if(parameterIDs != null && !parameterIDs.isEmpty())
                ParameterComboBox.setSelectedItem(parameterIDs.get(0));
        }
        else if(answerType.equals(Answer_ITEMS[1])){ //Result Tag
            AnswerTagTextField.setVisible(false);
            AnswerTagTextField.setText("");
            
            ResultTag2ComboBox.setVisible(true);
            
            ParameterComboBox.setVisible(false);
            if(parameterIDs != null && !parameterIDs.isEmpty())
                ParameterComboBox.setSelectedItem(parameterIDs.get(0));
        }
        else if(answerType.equals(Answer_ITEMS[2]) || answerType.equals(Answer_ITEMS[3])){
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
        goalsUI.data.updateListofGoals(goalsUI.getPanelofGoals());
        goalsUI.data.swapGoals(type, rowIndex);
        goalsUI.loadUI();
    }
  
    public void updateParameters(){
        String current = (String) ParameterComboBox.getSelectedItem();
        parameterIDs = dataUI.getParameters();
        ParameterComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(parameterIDs.toArray(new String[parameterIDs.size()])));
        if(parameterIDs.contains(current)){
            ParameterComboBox.setSelectedItem(current);
        }else{
            String id = getGoalIDTextField().getText();
            System.out.println("ERROR, goal "+id+" parameter of "+current+" was removed from parameters.");
       } 
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
    
    public String getComments(){
        return this.comments;
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
        ToolTipWrapper tip = ParamReferenceStorage.getWrapper(Answer_ITEMS, v);
        AnswerTypeComboBox.setSelectedItem(tip);
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
    private javax.swing.JComboBox<ToolTipWrapper> AnswerTypeComboBox;
    private javax.swing.JTextField ArithmeticResultTagTextField;
    private javax.swing.JPanel ArtifactPanel;
    private javax.swing.JComboBox<String> BooleanResultTagsComboBox;
    private javax.swing.JTextField BooleanTextField;
    private javax.swing.JButton DeleteButton;
    private javax.swing.JButton DocButton;
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
