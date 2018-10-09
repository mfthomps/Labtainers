/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ResultsUI;

import java.awt.Component;
import javax.swing.DefaultListCellRenderer;
import javax.swing.JComboBox;
import javax.swing.JComponent;
import javax.swing.JList;

/**
 *
 * @author Dan
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
    public static void setComboItems(JComboBox combobox, ToolTipWrapper[] items){
        ComboBoxRenderer renderer = new ComboBoxRenderer();
        combobox.setRenderer(renderer);
        
        for (ToolTipWrapper item : items) {
            combobox.addItem(item);
        }
    }
}
