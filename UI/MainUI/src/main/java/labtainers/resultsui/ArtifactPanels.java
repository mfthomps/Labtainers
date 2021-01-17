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
package labtainers.resultsui;

import java.awt.Dimension;
import java.util.ArrayList;
import javax.swing.DefaultComboBoxModel;
import javax.swing.JComboBox;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.JDialog;
import static labtainers.resultsui.ParamReferenceStorage.FieldType_ITEMS;
import static labtainers.resultsui.ParamReferenceStorage.LOG_ACCESIBLE_FieldType;
import static labtainers.resultsui.ParamReferenceStorage.LOG_TS_ACCESSIBLE_LineType;
import static labtainers.resultsui.ParamReferenceStorage.LineType_ITEMS;
import static labtainers.resultsui.ParamReferenceStorage.SpecialTimeStampType;
import static labtainers.resultsui.ParamReferenceStorage.TimestampType_ITEMS;
import static labtainers.resultsui.ParamReferenceStorage.justFieldType;
import static labtainers.resultsui.ParamReferenceStorage.lineParamAccessible;
import static labtainers.resultsui.ParamReferenceStorage.timeStampDelimiterAccessible;
import labtainers.mainui.ToolTipHandlers.ToolTipWrapper;
import labtainers.mainui.ToolTipHandlers.ToolTipWrapper;
import labtainers.goalsui.DocPanel;
import static labtainers.mainui.ToolTipHandlers.setComboItems;

/**
 *
 * @author Daniel Liao
 */
public class ArtifactPanels extends javax.swing.JPanel {

    static Dimension dim = new Dimension(975, 100);
    ResultsUI uiResult;
    ResultsData dataUI;
    int rowNum;
    String comments="";
    
    /**
     * Creates new form ArtifactsPanel
     */
    //Creating fresh artifact line
    public ArtifactPanels(ResultsUI ui, ArrayList<String> containers, int rowNum) {
        initComponents();
        this.uiResult = ui;
        this.dataUI = ui.data;
        this.rowNum = rowNum;
        
        jLabel3.setText(Integer.toString(rowNum));
        TimeDelimiterTextField.setVisible(false);
                
        //Load ComboBox Items
         if(containers.size() > 1 && !containers.contains("ALL"))
            containers.add(0, "ALL");
        ContainerComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(containers.toArray(new String[containers.size()])));   
        setComboItems(FieldTypeComboBox, FieldType_ITEMS);
        setComboItems(LineTypeComboBox, LineType_ITEMS);
        setComboItems(TimeStampComboBox, TimestampType_ITEMS);   
    }

    //Loading artifact line
    public ArtifactPanels(ResultsUI ui, ArrayList<String> containers, int rowNum, String resultTag, String container, String fileID, ToolTipWrapper fieldType, String fieldID, ToolTipWrapper lineType, String lineID, ToolTipWrapper timeStampType, String timeStampDelimiter, String comments) {
        initComponents();
        this.uiResult = ui;
        this.dataUI = ui.data;
        this.rowNum = rowNum;
        this.comments = comments;
        jLabel3.setText(Integer.toString(rowNum));      
        if(!timeStampDelimiterAccessible.contains(timeStampType.getItem()))
            TimeDelimiterTextField.setVisible(false);
        
        //Load ComboBox Items
        if(containers.size() > 1 && !containers.contains("ALL"))
            containers.add(0, "ALL");
        else if(containers.size() == 2 && containers.contains("ALL"))
            containers.remove("ALL");
        ContainerComboBox.setModel(new javax.swing.DefaultComboBoxModel<>(containers.toArray(new String[containers.size()])));
        setComboItems(FieldTypeComboBox, FieldType_ITEMS);
        setComboItems(LineTypeComboBox, LineType_ITEMS);
        setComboItems(TimeStampComboBox, TimestampType_ITEMS);
        
        //Set Values
        setContainerComboBox(container);       
        setFieldIDTextField(fieldID);      
        setTagTextField(resultTag);
        setFileTextField(fileID);        
        setFieldTypeComboBox(fieldType);         
        setLineIDTextField(lineID);         
        setLineTypeComboBox(lineType);          
        setTimeStampComboBox(timeStampType);          
        setTimeDelimiterTextField(timeStampDelimiter);
 
        this.revalidate();
        this.repaint();
    }
    
    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        jLabel3 = new javax.swing.JLabel();
        jButton1 = new javax.swing.JButton();
        UpButton = new javax.swing.JButton();
        DownButton = new javax.swing.JButton();
        ArtifactPanel = new javax.swing.JPanel();
        TagTextField = new javax.swing.JTextField();
        ContainerComboBox = new javax.swing.JComboBox<>();
        FileTextField = new javax.swing.JTextField();
        FieldTypeComboBox = new javax.swing.JComboBox<>();
        FieldIDTextField = new javax.swing.JTextField();
        LineTypeComboBox = new javax.swing.JComboBox<>();
        LineIDTextField = new javax.swing.JTextField();
        TimeStampComboBox = new javax.swing.JComboBox<>();
        TimeDelimiterTextField = new javax.swing.JTextField();
        DocButton = new javax.swing.JButton();

        setBorder(javax.swing.BorderFactory.createEtchedBorder());
        setMaximumSize(new java.awt.Dimension(1560, 86));
        setMinimumSize(new java.awt.Dimension(1560, 86));
        setName(""); // NOI18N
        setPreferredSize(new java.awt.Dimension(1580, 86));

        jLabel3.setFont(new java.awt.Font("Ubuntu", 1, 48)); // NOI18N
        jLabel3.setText("10");

        jButton1.setText("Delete");
        jButton1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton1ActionPerformed(evt);
            }
        });

        UpButton.setFont(new java.awt.Font("Ubuntu Condensed", 0, 12)); // NOI18N
        UpButton.setText("^");
        UpButton.setMaximumSize(new java.awt.Dimension(19, 50));
        UpButton.setMinimumSize(new java.awt.Dimension(19, 31));
        UpButton.setPreferredSize(new java.awt.Dimension(19, 31));
        UpButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                UpButtonActionPerformed(evt);
            }
        });

        DownButton.setFont(new java.awt.Font("Ubuntu Condensed", 0, 12)); // NOI18N
        DownButton.setText("v");
        DownButton.setToolTipText("");
        DownButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                DownButtonActionPerformed(evt);
            }
        });

        ArtifactPanel.setBorder(javax.swing.BorderFactory.createEmptyBorder(1, 1, 1, 1));

        FieldTypeComboBox.addItemListener(new java.awt.event.ItemListener() {
            public void itemStateChanged(java.awt.event.ItemEvent evt) {
                FieldTypeComboBoxItemStateChanged(evt);
            }
        });

        FieldIDTextField.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createEtchedBorder(), "Field ID"));

        LineTypeComboBox.setToolTipText("Identifies how the line is to be located.");
        LineTypeComboBox.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createEtchedBorder(), "Line Type"));
        LineTypeComboBox.addItemListener(new java.awt.event.ItemListener() {
            public void itemStateChanged(java.awt.event.ItemEvent evt) {
                LineTypeComboBoxItemStateChanged(evt);
            }
        });

        LineIDTextField.setToolTipText("Parameter based on Line Type");
        LineIDTextField.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createEtchedBorder(), "Line ID"));

        TimeStampComboBox.setToolTipText("<html>Source of time stamps, e.g., from the file<br>or from log entries</html>");
        TimeStampComboBox.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createEtchedBorder(), "Timestamp Type"));
        TimeStampComboBox.addItemListener(new java.awt.event.ItemListener() {
            public void itemStateChanged(java.awt.event.ItemEvent evt) {
                TimeStampComboBoxItemStateChanged(evt);
            }
        });

        TimeDelimiterTextField.setHorizontalAlignment(javax.swing.JTextField.LEFT);
        TimeDelimiterTextField.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createEtchedBorder(), "Time Delimiter"));
        TimeDelimiterTextField.setMinimumSize(new java.awt.Dimension(20, 100));

        javax.swing.GroupLayout ArtifactPanelLayout = new javax.swing.GroupLayout(ArtifactPanel);
        ArtifactPanel.setLayout(ArtifactPanelLayout);
        ArtifactPanelLayout.setHorizontalGroup(
            ArtifactPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(ArtifactPanelLayout.createSequentialGroup()
                .addContainerGap()
                .addComponent(TagTextField, javax.swing.GroupLayout.PREFERRED_SIZE, 138, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(ContainerComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, 134, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(FileTextField, javax.swing.GroupLayout.PREFERRED_SIZE, 138, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(FieldTypeComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, 160, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(FieldIDTextField, javax.swing.GroupLayout.PREFERRED_SIZE, 146, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(LineTypeComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, 165, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(LineIDTextField, javax.swing.GroupLayout.PREFERRED_SIZE, 142, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(TimeStampComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, 143, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(TimeDelimiterTextField, javax.swing.GroupLayout.PREFERRED_SIZE, 124, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );
        ArtifactPanelLayout.setVerticalGroup(
            ArtifactPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(ArtifactPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                .addComponent(TimeDelimiterTextField, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addComponent(TimeStampComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addComponent(LineIDTextField, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addComponent(LineTypeComboBox)
                .addComponent(FieldIDTextField, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
            .addGroup(ArtifactPanelLayout.createSequentialGroup()
                .addGroup(ArtifactPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(ArtifactPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                        .addComponent(FileTextField, javax.swing.GroupLayout.PREFERRED_SIZE, 40, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(FieldTypeComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, 40, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addGroup(ArtifactPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                        .addComponent(TagTextField, javax.swing.GroupLayout.PREFERRED_SIZE, 40, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(ContainerComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, 40, javax.swing.GroupLayout.PREFERRED_SIZE)))
                .addGap(0, 0, Short.MAX_VALUE))
        );

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
                .addComponent(jLabel3)
                .addGap(6, 6, 6)
                .addComponent(ArtifactPanel, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(DownButton, javax.swing.GroupLayout.PREFERRED_SIZE, 33, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(UpButton, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.PREFERRED_SIZE, 33, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jButton1)
                    .addComponent(DocButton))
                .addGap(23, 23, 23))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addContainerGap()
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                            .addComponent(ArtifactPanel, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(jLabel3)))
                    .addGroup(layout.createSequentialGroup()
                        .addGap(6, 6, 6)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(UpButton, javax.swing.GroupLayout.PREFERRED_SIZE, 31, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(jButton1))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(DownButton, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                            .addComponent(DocButton))))
                .addContainerGap())
        );
    }// </editor-fold>//GEN-END:initComponents

    private void UpButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_UpButtonActionPerformed
         swapUpdate("UP", rowNum-1); //Subtract rowNum by one to get the proper index number
    }//GEN-LAST:event_UpButtonActionPerformed

    private void DownButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_DownButtonActionPerformed
         swapUpdate("DOWN", rowNum-1); //Subtract rowNum by one to get the proper index number
    }//GEN-LAST:event_DownButtonActionPerformed

    private void FieldTypeComboBoxItemStateChanged(java.awt.event.ItemEvent evt) {//GEN-FIRST:event_FieldTypeComboBoxItemStateChanged
        fieldTypeListener();
    }//GEN-LAST:event_FieldTypeComboBoxItemStateChanged

    private void LineTypeComboBoxItemStateChanged(java.awt.event.ItemEvent evt) {//GEN-FIRST:event_LineTypeComboBoxItemStateChanged
        lineTypeListener();
    }//GEN-LAST:event_LineTypeComboBoxItemStateChanged

    private void TimeStampComboBoxItemStateChanged(java.awt.event.ItemEvent evt) {//GEN-FIRST:event_TimeStampComboBoxItemStateChanged
        timeStampListener();
    }//GEN-LAST:event_TimeStampComboBoxItemStateChanged

    private void jButton1ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton1ActionPerformed
        deleteButton();
    }//GEN-LAST:event_jButton1ActionPerformed

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
        dialog.setTitle("Documentation for "+TagTextField.getText());
        dialog.setVisible(true);
        if(panel.isOK()){
            this.comments = panel.getDoc();
        }
    }//GEN-LAST:event_DocButtonActionPerformed
    
    private void deleteButton(){
       JPanel panelOfArtifacts = (JPanel)this.getParent();
       panelOfArtifacts.remove(this);
       uiResult.data.rowCount--;
       uiResult.refresh();
    }
    private void lineTypeTimeStamp(ToolTipWrapper lineType){
        if(LOG_TS_ACCESSIBLE_LineType.contains(lineType.getItem())){               
            //Add "LOG_TS" to the timestampComboBox if it's not already
            if(((DefaultComboBoxModel)TimeStampComboBox.getModel()).getIndexOf(SpecialTimeStampType[0]) == -1) {
                TimeStampComboBox.addItem(SpecialTimeStampType[0]);
            }
            TimeStampComboBox.setVisible(true);
        }else{
            ToolTipWrapper fieldTypeTTW = (ToolTipWrapper)FieldTypeComboBox.getSelectedItem();
            //Remove "LOG_TS" from the timestampComboBox if it's not already
            if(((DefaultComboBoxModel)TimeStampComboBox.getModel()).getIndexOf(SpecialTimeStampType[0]) != -1 && !LOG_ACCESIBLE_FieldType.contains(fieldTypeTTW.getItem())) {
                TimeStampComboBox.removeItem(SpecialTimeStampType[0]);
            }
            TimeStampComboBox.setVisible(false);
        }
    } 
    
    //The listeners sees what values are present in their respective fields and then changes the interface based on that(remove or adding other fields)
    private void lineTypeListener(){
        ToolTipWrapper lineType = (ToolTipWrapper)LineTypeComboBox.getSelectedItem();
        
        if(lineType.getItem().equals("NONE")){
            LineIDTextField.setVisible(false);
        }
        else
            LineIDTextField.setVisible(true);
      
        //Does the line type allow for LOG_TS option in the TimeStampComboBox?
        lineTypeTimeStamp(lineType);    

        
        this.revalidate();
        this.repaint();
    }
   
    private void adjustFieldIDToolTip(String fieldType){
        //System.out.println("field type "+fieldType);
        String tip = FieldIDTextField.getToolTipText();
        switch(fieldType){
            case "TOKEN":
                tip = "Result is the Nth space-delimited token, where N is this integer.";
                break;
            case "QUOTES":
                tip = "Result is the Nth quoted string, where N is this integer.";
                break;
            case "PARENS":
                tip = "Result is the Nth string in parenthesis, where N is this integer.";
                break;
            case "SLASH":
                tip = "Result is the Nth slash-delimited token, where N is this integer.";
                break;
            case "CONTAINS":
                tip = "Result is true if the file contains this string.";
                break;
            case "FILE_REGEX":
                tip = "Result is true if the file contains this regular expression.";
                break;
            case "LOG_TS":
                tip = "Used with timestamped log files, results in a timestamped set of boolean results with a value of TRUE for each log line that contains this string.";
                break;
            case "FILE_REGEX_TS":
                tip = "Used with timestamped log files, results in a timestamped set of boolean results with a value of TRUE for each log line that contains this regular expression.";
                break;
            case "LOG_RANGE":
                tip = "Used with timestamped log files, results in a timestamped set of boolean results with a value of TRUE for each log line that contains this string, with timestamp ranges delimited by the matching log entries.";
                break;
            case "STRING_COUNT":
                tip = "The result value is set to the quantity of occurances of this string in the file.";
                break;
            case "COMMAND_COUNT": 
                tip = "Intended for use with bash_history files, counts the occurances of this command.  Commands are evaluated considering use of sudo, time, etc.";
                break;
            case "SEARCH":
                tip = "Result is assigned the value of string, which is treated as an expression having the syntax of pythons parse.search function.  E.g., 'frame.number=={:d}' would yield the frame number.";
                break;
            case "GROUP":
                tip = "Intended for use with 'REGEX' line types, the result is set to the value of the regex group number named by this value.  Regular expressions and their groups are processed using the python re.search semantics.";
                break;



            default:
                //System.out.println("adjustFieldIDToolTip no match");
        }
        FieldIDTextField.setToolTipText(tip);
    } 
    private void fieldTypeListener(){  
        ToolTipWrapper fieldType = (ToolTipWrapper)FieldTypeComboBox.getSelectedItem();
        adjustFieldIDToolTip(fieldType.getItem()); 
        //Does the fieldType allow for certain user inputs
        if(!justFieldType.contains(fieldType.getItem())){
            FieldIDTextField.setVisible(true);
            if(lineParamAccessible.contains(fieldType.getItem())){
                LineTypeComboBox.setVisible(true);
                LineIDTextField.setVisible(true);
            }
            else{
               setLineTypeComboBox(LineType_ITEMS[0]);
               LineTypeComboBox.setVisible(false);
               setLineIDTextField("");
               LineIDTextField.setVisible(false); 
            }         
        }
        else{
            setFieldIDTextField("");
            FieldIDTextField.setVisible(false);
            setLineTypeComboBox(LineType_ITEMS[0]);
            LineTypeComboBox.setVisible(false);
            setLineIDTextField("");
            LineIDTextField.setVisible(false);
        }
       
        /*
        If the selected Field Type allows for the "LOG_TS" and "LOG_RANGE" in the timeStampComboBox, 
        then make sure to add them if they aren't there already
        */
        if(LOG_ACCESIBLE_FieldType.contains(fieldType.getItem())){
            //Add "LOG_TS" to the timestampComboBox if it's not already
            if(((DefaultComboBoxModel)TimeStampComboBox.getModel()).getIndexOf(SpecialTimeStampType[0]) == -1){
                TimeStampComboBox.addItem(SpecialTimeStampType[0]);
            }
            //Add "LOG_RANGE" to the timestampComboBox if it's not already
            if(((DefaultComboBoxModel)TimeStampComboBox.getModel()).getIndexOf(SpecialTimeStampType[1]) == -1){
                TimeStampComboBox.addItem(SpecialTimeStampType[1]);          
            }
            TimeStampComboBox.setVisible(true);
        }
        /*
        If the selcted Field Type doesn't allow for "LOG_TS" and "LOG_RANGE" in the timeStampComboBox, 
        then make sure to remove them if they're still in the box
        */
        else{
            ToolTipWrapper lineType = (ToolTipWrapper)LineTypeComboBox.getSelectedItem();
            //Remove "LOG_TS" from the timestampComboBox if it's not already
            if(((DefaultComboBoxModel)TimeStampComboBox.getModel()).getIndexOf(SpecialTimeStampType[0]) != -1 && !LOG_TS_ACCESSIBLE_LineType.contains(lineType.getItem())){
                TimeStampComboBox.removeItem(SpecialTimeStampType[0]);
            }
            //Remove "LOG_RANGE" from the timestampComboBox if it's there
            if(((DefaultComboBoxModel)TimeStampComboBox.getModel()).getIndexOf(SpecialTimeStampType[1]) != -1){
                TimeStampComboBox.removeItem(SpecialTimeStampType[1]);          
            }
            TimeStampComboBox.setVisible(false);
        }
        
        ArtifactPanel.revalidate();
        ArtifactPanel.repaint();
    }
    
    private void timeStampListener(){
        ToolTipWrapper timestamptype = (ToolTipWrapper)TimeStampComboBox.getSelectedItem();
        //Does the timestamp Type allow for Time Delimiter input
        if(timeStampDelimiterAccessible.contains(timestamptype.getItem()))
            TimeDelimiterTextField.setVisible(true);
        else{
            setTimeDelimiterTextField("");
            TimeDelimiterTextField.setVisible(false);
        }
        ArtifactPanel.revalidate();
        ArtifactPanel.repaint();
    }
    
    //Swaps artifact order in the list of artifacts and then redraws them
    void swapUpdate(String type, int rowIndex){
        //System.out.println("RowCOUNT(swap): " +dataUI.rowCount);
        dataUI.updateListofArtifacts(uiResult.getPanelofArtifacts());
        dataUI.swapArtifacts(type, rowIndex);
        uiResult.loadUI();
    }
    
        //Field Getters
    public JComboBox<String> getContainerComboBox(){
        return ContainerComboBox;
    }    
    public JTextField getFieldIDTextField(){
        return FieldIDTextField;
    }
    public JTextField getTagTextField(){
        return TagTextField;
    }
    public JTextField getFileTextField(){
        return FileTextField;
    }
    public JComboBox<ToolTipWrapper> getFieldTypeComboBox(){
        return FieldTypeComboBox;
    }
    public JTextField getLineIDTextField(){
        return LineIDTextField;
    }
    public JComboBox<ToolTipWrapper> getLineTypeComboBox(){
        return LineTypeComboBox;
    }    
    public JComboBox<ToolTipWrapper> getTimeStampComboBox(){
        return TimeStampComboBox;
    }
    public JTextField getTimeStampTextField(){
        return TimeDelimiterTextField;
    }
    public String getComments(){
        return this.comments;
    }

    //Field SETTERS
    private void setContainerComboBox(String v){
        ContainerComboBox.setSelectedItem(v);
    }    
    private void setFieldIDTextField(String v){
        FieldIDTextField.setText(v);
    }
    private void setTagTextField(String v){
        TagTextField.setText(v);
    }
    private void setFileTextField(String v){
        FileTextField.setText(v);
    }
    private void setFieldTypeComboBox(ToolTipWrapper v){
        FieldTypeComboBox.setSelectedItem(v);
    }
    private void setLineIDTextField(String v){
        LineIDTextField.setText(v);
    }
    private void setLineTypeComboBox(ToolTipWrapper v){
        LineTypeComboBox.setSelectedItem(v);
    }    
    private void setTimeStampComboBox(ToolTipWrapper v){
        TimeStampComboBox.setSelectedItem(v);
    }
    private void setTimeDelimiterTextField(String v){
        TimeDelimiterTextField.setText(v);
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JPanel ArtifactPanel;
    private javax.swing.JComboBox<String> ContainerComboBox;
    private javax.swing.JButton DocButton;
    private javax.swing.JButton DownButton;
    private javax.swing.JTextField FieldIDTextField;
    private javax.swing.JComboBox<ToolTipWrapper> FieldTypeComboBox;
    private javax.swing.JTextField FileTextField;
    private javax.swing.JTextField LineIDTextField;
    private javax.swing.JComboBox<ToolTipWrapper> LineTypeComboBox;
    private javax.swing.JTextField TagTextField;
    private javax.swing.JTextField TimeDelimiterTextField;
    private javax.swing.JComboBox<ToolTipWrapper> TimeStampComboBox;
    private javax.swing.JButton UpButton;
    private javax.swing.JButton jButton1;
    private javax.swing.JLabel jLabel3;
    // End of variables declaration//GEN-END:variables
}
