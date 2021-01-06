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
package labtainers.mainui;

import java.awt.Component;
import javax.swing.DefaultComboBoxModel;
import javax.swing.DefaultListCellRenderer;
import javax.swing.JComboBox;
import javax.swing.JComponent;
import javax.swing.JList;

/**
 *
 * @author student
 */
public class ToolTipHandlers {
    public static interface ToolTipProvider{
        public String getToolTip();
    }
    
    //Stores an item and its correspoinding tool tip. (Items put into a combobox)
    public static class ToolTipWrapper implements ToolTipProvider{
        final String item;
        final String toolTip;
        
        public ToolTipWrapper(String item, String toolTip){
            this.item = item;
            this.toolTip = toolTip;
        }
        
        @Override
        public String getToolTip(){
            return toolTip;
        }
        
        @Override
        public String toString(){
            return item;
        }
        
        public String getItem(){
            return item;
        }
    }
    
    //custom combobox renderer to handle ToolTipWrapper objects that contain an string item and string tool tip
    public static class ComboBoxRenderer extends DefaultListCellRenderer {
    
        @Override
        public Component getListCellRendererComponent(JList list, Object value, int index, boolean isSelected, boolean cellHasFocus) {
            JComponent component = (JComponent) super.getListCellRendererComponent(list, value, index, isSelected, cellHasFocus);
            String tip = null;
            if (value instanceof ToolTipProvider) {
                ToolTipProvider ttp = (ToolTipProvider) value;
                tip = ttp.getToolTip();
            }
            list.setToolTipText(tip);
            return component;
        }
    }
    
  //Sets the combo items with associated tool tips (called in the constructors)
    public static void setComboItems(JComboBox <ToolTipWrapper>combobox, ToolTipWrapper[] items){
        ComboBoxRenderer renderer = new ComboBoxRenderer();
        combobox.setRenderer(renderer);
        
        for (ToolTipWrapper item : items) {
            if(((DefaultComboBoxModel)combobox.getModel()).getIndexOf(item) == -1) 
            combobox.addItem(item);
        }
    }
}
