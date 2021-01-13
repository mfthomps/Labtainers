package labtainers.paramsui;

/*
 * TableRenderDemo.java requires no other files.
 */

import java.util.ArrayList;
import javax.swing.DefaultCellEditor;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.table.AbstractTableModel;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.TableCellRenderer;
import javax.swing.table.TableColumn;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.GridLayout;
import java.awt.event.MouseEvent;
import java.awt.event.MouseMotionAdapter;
import java.util.HashMap;
import java.util.Map;

import javax.swing.JTable;
import javax.swing.table.JTableHeader;
import javax.swing.table.TableColumnModel;

/** 
 
 */
public class ContainerFileTable extends JPanel {
    private boolean DEBUG = true;
    private boolean multipleContainers = false;
    private JTable table;
    private ArrayList<String> containers;
    public ContainerFileTable(ArrayList<String> containers, ArrayList<String> fileList) {
        super(new GridLayout(1,0));

        this.table = new JTable(new MyTableModel());
        this.containers = containers;
        addList(fileList);
        this.table.setRowSelectionInterval(0, 0);
        table.setPreferredScrollableViewportSize(new Dimension(500, 70));
        table.setFillsViewportHeight(true);

        JScrollPane scrollPane = new JScrollPane(table);

        initColumnSizes(table);

        setUpContainersColumn(table, table.getColumnModel().getColumn(0), containers);

        add(scrollPane);
        if(containers.size() > 1){
            multipleContainers = true;
        }


        JTableHeader header = table.getTableHeader();

        ColumnHeaderToolTips tips = new ColumnHeaderToolTips();
        TableColumn container_col = this.table.getColumnModel().getColumn(0);
        tips.setToolTip(container_col, "<html>Click for combo box, select container whose file is to be modified or start.config<br> or select start.config to modify configuration values, e.g., IP addresses.");
        TableColumn file_col = this.table.getColumnModel().getColumn(1);
        tips.setToolTip(file_col, "<html>Absolute path of the file to be modifed on the container.");
        header.addMouseMotionListener(tips);
    }
    public ArrayList<String> getFileList(){
        MyTableModel model = (MyTableModel)this.table.getModel();
        return model.getFileList(this.multipleContainers);
    }
    private void addList(ArrayList<String> fileList){
        MyTableModel model = (MyTableModel)this.table.getModel();
        if(fileList != null && fileList.size() > 0){
            for(String item : fileList){
                System.out.println("addList item "+item);
                String container = "";
                String file = "";
                if(item.contains(":")){
                    String[] parts = item.split(":");
                    container = parts[0];
                    if(parts.length > 1){
                        file = parts[1];
                    }
                }else if(item.equals("start.config")){
                    container = item;
                }else{
                    file = item;
                    container = this.containers.get(0);
                }
                model.addRow(container, file);
            } 
        }else{
            String container = this.containers.get(0);
            model.addRow(container, "");
        }
    }
    public void addRow(){
        MyTableModel model = (MyTableModel)this.table.getModel();
        String container = this.containers.get(0);
        model.addRow(container, "");
        int last = model.getRowCount()-1;
        this.table.setRowSelectionInterval(last, last);
    } 
    public void deleteRow(){
        int selected = this.table.getSelectedRow();
        if(selected >=0){
            MyTableModel model = (MyTableModel)this.table.getModel();
            model.deleteRow(selected);
            this.table.setRowSelectionInterval(0, 0);
        }
    } 
    /*
     * This method picks good column sizes.
     * If all column heads are wider than the column's cells'
     * contents, then you can just use column.sizeWidthToFit().
     */
    private void initColumnSizes(JTable table) {
        MyTableModel model = (MyTableModel)table.getModel();
        TableColumn column = null;
        Component comp = null;
        int headerWidth = 0;
        int cellWidth = 0;
        Object[] longValues = model.longValues;
        TableCellRenderer headerRenderer =
            table.getTableHeader().getDefaultRenderer();

        for (int i = 0; i < 1; i++) {
            column = table.getColumnModel().getColumn(i);

            comp = headerRenderer.getTableCellRendererComponent(
                                 null, column.getHeaderValue(),
                                 false, false, 0, 0);
            headerWidth = comp.getPreferredSize().width;

            comp = table.getDefaultRenderer(model.getColumnClass(i)).
                             getTableCellRendererComponent(
                                 table, longValues[i],
                                 false, false, 0, i);
            cellWidth = comp.getPreferredSize().width;

            if (DEBUG) {
                System.out.println("Initializing width of column "
                                   + i + ". "
                                   + "headerWidth = " + headerWidth
                                   + "; cellWidth = " + cellWidth);
            }

            column.setPreferredWidth(Math.max(headerWidth, cellWidth));
        }
    }

    public void setUpContainersColumn(JTable table,
                                 TableColumn containerColumn, ArrayList<String> containers) {
        //Set up the editor for the container column.
        JComboBox<String> comboBox = new JComboBox<String>();
        for(String c : containers){
            comboBox.addItem(c);
        }
        comboBox.addItem("start.config");
        
        containerColumn.setCellEditor(new DefaultCellEditor(comboBox));

        //Set up tool tips for the container cells.
        DefaultTableCellRenderer renderer =
                new DefaultTableCellRenderer();
        renderer.setToolTipText("Click for combo box");
        containerColumn.setCellRenderer(renderer);
    }

    class ColumnHeaderToolTips extends MouseMotionAdapter {
      TableColumn curCol;
      Map<TableColumn, String> tips = new HashMap<TableColumn, String>();
      public void setToolTip(TableColumn col, String tooltip) {
        if (tooltip == null) {
          tips.remove(col);
        } else {
          tips.put(col, tooltip);
        }
      }
      public void mouseMoved(MouseEvent evt) {
        JTableHeader header = (JTableHeader) evt.getSource();
        JTable table = header.getTable();
        TableColumnModel colModel = table.getColumnModel();
        int vColIndex = colModel.getColumnIndexAtX(evt.getX());
        TableColumn col = null;
        if (vColIndex >= 0) {
          col = colModel.getColumn(vColIndex);
        }
        if (col != curCol) {
          header.setToolTipText((String) tips.get(col));
          curCol = col;
        }
      }
    }
    class MyTableModel extends AbstractTableModel {
        private String[] columnNames = {"Container",
                                        "File"};
        //private Object[][] data = {
        //};
        private ArrayList<String[]> data = new ArrayList<String[]>();
        public void addRow(String container, String file){
            System.out.println("addRow "+container+":"+file);
            String[] entry = {container, file};
            data.add(entry);
        }
        public void deleteRow(int row){
            data.remove(row);
            fireTableDataChanged();
        } 

        public final Object[] longValues = {"some container", "some file"};

        public int getColumnCount() {
            return columnNames.length;
        }

        public int getRowCount() {
            return data.size();
        }

        public String getColumnName(int col) {
            return columnNames[col];
        }

        public Object getValueAt(int row, int col) {
            String[] r = data.get(row);
            return r[col];
        }

        /*
         * JTable uses this method to determine the default renderer/
         * editor for each cell.  If we didn't implement this method,
         * then the last column would contain text ("true"/"false"),
         * rather than a check box.
         */
        public Class getColumnClass(int c) {
            return getValueAt(0, c).getClass();
        }

        /*
         * Don't need to implement this method unless your table's
         * editable.
         */
        public boolean isCellEditable(int row, int col) {
            return true;
        }

        /*
         * Don't need to implement this method unless your table's
         * data can change.
         */
        public void setValueAt(Object value, int row, int col) {
            if(row < getRowCount()){
                if (DEBUG) {
                    System.out.println("Setting value at " + row + "," + col
                                       + " to " + value
                                       + " (an instance of "
                                       + value.getClass() + ")");
                }
                String[] r = data.get(row);
                r[col] = (String) value;
                fireTableCellUpdated(row, col);

                if (DEBUG) {
                    System.out.println("New value of data:");
                    printDebugData();
                }
            }
        }

        private void printDebugData() {
            int numRows = getRowCount();
            int numCols = getColumnCount();

            for (int i=0; i < numRows; i++) {
                System.out.print("    row " + i + ":");
                for (int j=0; j < numCols; j++) {
                    //System.out.print("  " + data[i][j]);
                }
                System.out.println();
            }
            System.out.println("--------------------------");
        }
        public ArrayList<String> getFileList(boolean multipleContainers){
            ArrayList<String> retval = new ArrayList<String>();
            String containerFile = "";
            for(String[] row : this.data){
                String container = row[0];
                String file = row[1];
                if(container.equals("start.config")){
                    containerFile = container;
                }else{
                    if(!multipleContainers){
                        containerFile = file;
                    }else{
                        containerFile = container+":"+file;
                    }
                } 
                retval.add(containerFile);
            }
            return retval;
        }
    }
}
