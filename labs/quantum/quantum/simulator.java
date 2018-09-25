import java.io.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;

class Complex
{
    double real;
    double imaginary;

    public Complex(double r, double i)
    {
	real = r;
	imaginary = i;
    }

    public void assign(double r, double i)
    {
	real = r;
	imaginary = i;
	return;
    }

    public void assign(Complex c)
    {
	real = c.getReal();
	imaginary = c.getImaginary();
	return;
    }
    
    public void add(Complex comp)
    {
	double a = real;
	double b = imaginary;
	double c = comp.getReal();
	double d = comp.getImaginary();
	real = a+c;
	imaginary = b+d;
	return;
    }

    public void subtract(Complex comp)
    {
	double a = real;
	double b = imaginary;
	double c = comp.getReal();
	double d = comp.getImaginary();
	real = a-c;
	imaginary = b-d;
	return;
    }

    public void multiply(Complex comp)
    {
	double a = real;
	double b = imaginary;
	double c = comp.getReal();
	double d = comp.getImaginary();
	real = a*c-b*d;
	imaginary = b*c+a*d;
	return;
    }

    public void divide(Complex comp)
    {
	double a = real;
	double b = imaginary;
	double c = comp.getReal();
	double d = comp.getImaginary();
	double denominator = c*c+d*d;
	real = (a*c+b*d)/denominator;
	imaginary = (b*c-a*d)/denominator;
	return;
    }

    public void scale(double factor)
    {
	double a = real;
	double b = imaginary;
	real = a*factor;
	imaginary = b*factor;
	return;
    }

    public double getReal()
    {
	return real;
    }

    public double getImaginary()
    {
	return imaginary;
    }
}

class Matrix
{
    int m_w, m_h;
    Complex[][] m;

    public Matrix(int w, int h)
    {
	m_w = w;
	m_h = h;
	m = new Complex[h][w];
	for (int i = 0; i < h; i++) {
	    for (int j = 0; j < w; j++) {
		m[i][j] = new Complex(0.0,0.0);
	    }
	}
    }
    
    public void assign(int r, int c, Complex complex)
    {
	m[r][c].assign(complex);
    }

    public void assign(int r, int c, double real, double imaginary)
    {
	m[r][c].assign(real, imaginary);
    }

    public Complex getValue(int r, int c)
    {
	return m[r][c];
    }

    public int getWidth()
    {
	return m_w;
    }

    public int getHeight()
    {						
	return m_h;
    }

    public static Matrix combine(Matrix m1, Matrix m2)
    {
	Matrix m3 = new Matrix(m1.getWidth()*m2.getWidth(),
			      m1.getHeight()*m2.getHeight());
	for (int i = 0; i < m1.getWidth(); i++) {
	    for (int j = 0; j < m1.getHeight(); j++) {
		for (int k = 0; k < m2.getWidth(); k++) {
		    for (int l = 0; l < m2.getHeight(); l++) {
			Complex c = m3.getValue(j*m2.getHeight()+l,i*m2.getWidth()+k);
			c.assign(m1.getValue(j,i));
			c.multiply(m2.getValue(l,k));
		    }
		}
	    }
	} 
	return m3;
    }
    
    public static Matrix multiply(Matrix m1, Matrix m2)
    {
	Matrix m3 = new Matrix(m2.getWidth(),m1.getHeight());
	if (m1.getWidth() != m2.getHeight()) {
	    System.err.println("Cannot multiply incompatible matrices.");
	    System.err.println("Have a nice day.");
	    System.exit(1);
	}
	for (int i = 0; i < m1.getHeight(); i++) {
	    for (int j = 0; j < m2.getWidth(); j++) {
		Complex sum = m3.getValue(i,j);
		sum.assign(0.0,0.0);
		for (int k = 0; k < m1.getWidth(); k++) {
		    double a_real = m1.getValue(i,k).getReal();
		    double a_imaginary = m1.getValue(i,k).getImaginary();
		    double b_real = m2.getValue(k,j).getReal();
		    double b_imaginary = m2.getValue(k,j).getImaginary();
		    // Multiply a and b
		    double R = a_real * b_real - a_imaginary * b_imaginary;
		    double I = a_imaginary * b_real + a_real * b_imaginary;
		    // Add the product to sum
		    double s_r = sum.getReal();
		    double s_i = sum.getImaginary();
		    sum.assign(R+s_r,I+s_i);
		}
	    }
	}
	return m3;
    }

    public String print()
    {
	return print(true);
    }

    public String print(boolean ket)
    {
	String s = "";
	for (int row = 0; row < m_h; row++) {
	    if (ket == true)
		s += "|" + row + "> ";
	    for (int col = 0; col < m_w; col++) {
		//s += "" + m[row][col].getReal()+" ";
		s += "" + m[row][col].getReal()+"+"+m[row][col].getImaginary()+"i ";
	    }
	    s += "\n";
	}
	return s;
    }

    public String printNonzero()
    {
	String s = "";
	for (int row = 0; row < m_h; row++) {
	    boolean entirerowiszero = true;
	    for (int col = 0; col < m_w; col++) {
		double real = m[row][col].getReal();
		double complex = m[row][col].getImaginary();
		if (real != 0.0 || complex != 0.0) {
		    entirerowiszero = false;
		    if (col == 0) {
			s += "|" + row + "> ";
		    }
		    s += "" + m[row][col].getReal()+"+"+m[row][col].getImaginary()+"i ";
		} 
	    }
	    if (!entirerowiszero) {
		s += "\n";
	    }
	}
	return s;
    }
}

class qpanel extends Panel
{
    int m_w;
    int m_h;
    int m_n;
    int m_step;
    Matrix m_U;
    Matrix m_V;
    Vector m_phi0;
    Vector m_transforms;

    public qpanel(int width, int height)
    {
	m_step = 0;
	m_w=width;
	m_h=height;
    }

    public void setCircuitParameters(int n, Matrix U, Matrix V, Vector phi0, Vector transforms)
    {
	m_n = n;
	m_U = U;
	m_V = V;
	m_phi0 = phi0;
	m_transforms = transforms;
    }
    
    public Dimension getMinimumSize()
    {
	return new Dimension(m_w,m_h);
    }

    public Dimension getPreferredSize()
    {
	return new Dimension(m_w,m_h);
    }

    public void setStep(int step)
    {
	m_step = step;
    }

    public void paint(Graphics g)
    {
	g.setColor(Color.black);
	g.fillRect(0,0,m_w,m_h);
	g.setColor(Color.red);
	g.drawLine(100 + m_step * 100, 0, 100 + m_step * 100, m_h);
	g.setColor(Color.white);
	for (int i = 0; i < m_phi0.size(); i++) {
	    Integer I = (Integer)m_phi0.elementAt(i);
	    g.drawString("|"+I.intValue()+">",50,100 + 100*i);
	}
	for (int i = 0; i < m_transforms.size(); i++) {
	    Vector v = (Vector)m_transforms.elementAt(i);
	    int offset = 0;
	    for (int j = 0; j < v.size(); j++) { 
		String s = (String)v.elementAt(j);
		if (s.compareTo("I") == 0) {
		    g.drawLine(100 + i * 100, 90 + (j+offset) * 100, 200 + i * 100, 90 + (j+offset) * 100);
		} else if (s.compareTo("U") == 0) {
		    g.drawRect(110 + i * 100, 50 + j * 100, 80, 100*m_n-20);
		    g.drawString(s, 150 + i * 100, 40 + m_n * 50);
		    for (int k = 0; k < m_n; k++) {
			g.drawLine(100 + i * 100, 90 + k * 100, 110 + i * 100, 90 + k * 100);
			g.drawLine(190 + i * 100, 90 + k * 100, 200 + i * 100, 90 + k * 100);
		    }
		    offset += m_n;
		} else if (s.compareTo("CNOT") == 0) {
		    g.drawRect(110 + i * 100, 50 + (j+offset) * 100, 80, 100*2-20);
		    g.drawString(s, 130 + i * 100, 140 + (j+offset) * 100);
		    for (int k = 0; k < 2; k++) {
			g.drawLine(100 + i * 100, 90 + (j+offset+k) * 100, 110 + i * 100, 90 + (j+offset+k) * 100);
			g.drawLine(190 + i * 100, 90 + (j+offset+k) * 100, 200 + i * 100, 90 + (j+offset+k) * 100);
		    }
		    offset += 1;
		} else if (s.compareTo("V") == 0) {
		    g.drawRect(110 + i * 100, 50 + (j+offset) * 100, 80, 100*log2(m_V.getHeight())-20);
		    g.drawString(s, 150 + i * 100, 40 + (j+offset+log2(m_V.getHeight())) * 50);
		    for (int k = 0; k < log2(m_V.getHeight()); k++) {
			g.drawLine(100 + i * 100, 90 + (j+offset+k) * 100, 110 + i * 100, 90 + (j+offset+k) * 100);
			g.drawLine(190 + i * 100, 90 + (j+offset+k) * 100, 200 + i * 100, 90 + (j+offset+k) * 100);
		    }
		    offset += log2(m_V.getHeight()) - 1;
		} else if (s.compareTo("Control") == 0) {
		    g.drawRect(110 + i * 100, 50 + (j+offset) * 100, 80, 80);
		    g.drawString(s, 130 + i * 100, 100 + (j+offset) * 100);
		    g.drawLine(100 + i * 100, 90 + (j+offset) * 100, 110 + i * 100, 90 + (j+offset) * 100);
		    g.drawLine(190 + i * 100, 90 + (j+offset) * 100, 200 + i * 100, 90 + (j+offset) * 100);
		} else if (s.compareTo("Target") == 0 || s.compareTo("UCSP1") == 0 || s.compareTo("UCSP2") == 0 || s.compareTo("UCTP1") == 0 || s.compareTo("UCTP2") == 0 || s.compareTo("UCR41") == 0 || s.compareTo("UCR4P1") == 0 || s.compareTo("UCR42") == 0 || s.compareTo("UCR4P2") == 0) {
		    g.drawRect(110 + i * 100, 50 + (j+offset) * 100, 80, 80);
		    g.drawString(s, 130 + i * 100, 100 + (j+offset) * 100);
		    g.drawLine(100 + i * 100, 90 + (j+offset) * 100, 110 + i * 100, 90 + (j+offset) * 100);
		    g.drawLine(190 + i * 100, 90 + (j+offset) * 100, 200 + i * 100, 90 + (j+offset) * 100);
		} else if (s.compareTo("UT1") == 0 || s.compareTo("UT2") == 0 || s.compareTo("UT3") == 0) {
		    g.drawRect(110 + i * 100, 50 + (j+offset) * 100, 80, 80);
		    g.drawString(s, 140 + i * 100, 100 + (j+offset) * 100);
		    g.drawLine(100 + i * 100, 90 + (j+offset) * 100, 110 + i * 100, 90 + (j+offset) * 100);
		    g.drawLine(190 + i * 100, 90 + (j+offset) * 100, 200 + i * 100, 90 + (j+offset) * 100);
		} else if (s.compareTo("UCS1") == 0 || s.compareTo("UCS2") == 0 || s.compareTo("UCT1") == 0 || s.compareTo("UCT2") == 0 || s.compareTo("CTP1") == 0 || s.compareTo("CTP2") == 0 || s.compareTo("CSP1") == 0 || s.compareTo("CSP2") == 0) {
		    g.drawRect(110 + i * 100, 50 + (j+offset) * 100, 80, 80);
		    g.drawString(s, 135 + i * 100, 100 + (j+offset) * 100);
		    g.drawLine(100 + i * 100, 90 + (j+offset) * 100, 110 + i * 100, 90 + (j+offset) * 100);
		    g.drawLine(190 + i * 100, 90 + (j+offset) * 100, 200 + i * 100, 90 + (j+offset) * 100);
		} else if (s.compareTo("CS1") == 0 || s.compareTo("CS2") == 0 || s.compareTo("CT1") == 0 || s.compareTo("CT2") == 0) {
		    g.drawRect(110 + i * 100, 50 + (j+offset) * 100, 80, 80);
		    g.drawString(s, 140 + i * 100, 100 + (j+offset) * 100);
		    g.drawLine(100 + i * 100, 90 + (j+offset) * 100, 110 + i * 100, 90 + (j+offset) * 100);
		    g.drawLine(190 + i * 100, 90 + (j+offset) * 100, 200 + i * 100, 90 + (j+offset) * 100);
		} else if (s.compareTo("T1") == 0 || s.compareTo("T2") == 0 || s.compareTo("T3") == 0) {
		    g.drawRect(110 + i * 100, 50 + (j+offset) * 100, 80, 80);
		    g.drawString(s, 145 + i * 100, 100 + (j+offset) * 100);
		    g.drawLine(100 + i * 100, 90 + (j+offset) * 100, 110 + i * 100, 90 + (j+offset) * 100);
		    g.drawLine(190 + i * 100, 90 + (j+offset) * 100, 200 + i * 100, 90 + (j+offset) * 100);
		} else if (s.compareTo("S1") == 0 || s.compareTo("S2") == 0) {
		    g.drawRect(110 + i * 100, 50 + (j+offset) * 100, 80, 80);
		    g.drawString(s, 145 + i * 100, 100 + (j+offset) * 100);
		    g.drawLine(100 + i * 100, 90 + (j+offset) * 100, 110 + i * 100, 90 + (j+offset) * 100);
		    g.drawLine(190 + i * 100, 90 + (j+offset) * 100, 200 + i * 100, 90 + (j+offset) * 100);
		} else {
		    g.drawRect(110 + i * 100, 50 + (j+offset) * 100, 80, 80);
		    g.drawString(s, 150 + i * 100, 100 + (j+offset) * 100);
		    g.drawLine(100 + i * 100, 90 + (j+offset) * 100, 110 + i * 100, 90 + (j+offset) * 100);
		    g.drawLine(190 + i * 100, 90 + (j+offset) * 100, 200 + i * 100, 90 + (j+offset) * 100);
		}
	    }
	}
    }

    public int log2(int a)
    {
	int i = 0;
	for (int q = 1; q < a; i++, q *= 2);
	return i;
    }
}

class qframe extends Frame implements MouseListener, ItemListener, ActionListener
{
    int m_x, m_y;
    TextArea m_ta;
    Label m_labelStep;
    Button m_buttonStep;
    Button m_buttonAuto;
    qpanel m_p;
    ScrollPane m_sp;
    String m_fn;
    int m_fileNumber;
    Matrix m_U;
    Matrix m_V = null;
    Vector m_phi0;
    Vector m_transforms;
    Matrix m_currentPhi;
    Matrix m_measured;
    Matrix m_measurements;
    int m_n;
    int m_step;

    public qframe(String fn)
    {
        addWindowListener(new WindowAdapter(){
            public void windowClosing(WindowEvent e){
                dispose();
            }
        });
	m_fn = fn;
	m_fileNumber=0;
	m_step = 0;
	setSize(1100, 750);
	setBackground(Color.white);
	setLayout(null);
	m_labelStep = new Label("Proceed to next step");
	m_ta = new TextArea("", 100, 100, TextArea.SCROLLBARS_BOTH);
	m_labelStep.setBounds(0, 400, 512, 20);
	m_buttonStep = new Button("Next");
	m_buttonStep.setBounds(10, 420, 100, 20);
	m_buttonStep.addActionListener(this);
	m_buttonAuto = new Button("Auto");
	m_buttonAuto.setBounds(120, 420, 100, 20);
	m_buttonAuto.addActionListener(this);
	m_sp = new ScrollPane(ScrollPane.SCROLLBARS_ALWAYS);
	m_p = new qpanel(1700,1700);
	m_p.addMouseListener(this);
	m_sp.setSize(1024, 400);
	m_sp.add(m_p);
	m_ta.setBounds(512, 420, 512, 300);
	m_ta.setText("");
	add(m_sp);
	add(m_ta);
	add(m_labelStep);
	add(m_buttonStep);
	add(m_buttonAuto);
	setTitle("Simple Quantum Circuit Simulator");
	parse(m_fn);
	initializePhi();
	initializeMeasured();
    }
    
    public void parse(String fn)
    {
	m_transforms = new Vector();
	BufferedReader br = null;
	try {
	    br = new BufferedReader(new FileReader(fn));
	} catch (Exception e) {
	    handleEx(e);
	}
	while (true) {
	    String s = "";
	    try { s = br.readLine(); } catch (Exception e) { handleEx(e); }
	    if (s == null) break;
	    int index = s.indexOf("#");
	    if (index != -1) {
		s = s.substring(0, index);
	    }
	    m_ta.append(s+"\n");
	    if (s.indexOf("Define N ") == 0) {
		int n = 0;
		String N = "";
		for (int i = 9; i < s.length(); i++) {
		    if (Character.isDigit(s.charAt(i))) {
			N += s.charAt(i);
		    }
		}
		try {
		    n = Integer.parseInt(N);
		} catch (Exception e) { handleEx(e); }
		m_n = n;
	    } else if (s.indexOf("Define Phi0") == 0) {
		m_phi0 = new Vector();
		try { s = br.readLine(); } catch (Exception e) { handleEx(e); }
		if (s == null) break;
		index = s.indexOf("#");
		if (index != -1) {
		    s = s.substring(0, index);
		}
		m_ta.append(s+"\n");
		int count = 0;
		for (int j = 0; j < m_n; j++) {
		    String ELEM = "";
		    int elem = 0;
		    while (count < s.length() && !Character.isDigit(s.charAt(count))) {
			count++;
		    }
		    while (count < s.length() && Character.isDigit(s.charAt(count))) {
			ELEM += s.charAt(count);
			count++;
		    }
		    try {
			elem = Integer.parseInt(ELEM);
			m_phi0.add(new Integer(elem));
		    } catch (Exception e) { handleEx(e); }
		}
		//printPhi(m_phi0);
	    } else if (s.indexOf("Define Transform") == 0) {
		Vector transform = new Vector();
		try { s = br.readLine(); } catch (Exception e) { handleEx(e); }
		if (s == null) break;
		index = s.indexOf("#");
		if (index != -1) {
		    s = s.substring(0, index);
		}
		m_ta.append(s+"\n");
		int count = 0;
		for (int j = 0; j < m_n && count < s.length(); j++) {
		    String ELEM = "";
		    while (count < s.length() && !Character.isDigit(s.charAt(count)) && !Character.isLetter(s.charAt(count))) {
			count++;
		    }
		    while (count < s.length() && (Character.isDigit(s.charAt(count)) || Character.isLetter(s.charAt(count)))) {
			ELEM += s.charAt(count);
			count++;
		    }
		    if (ELEM.compareTo("") != 0)
			transform.add(new String(ELEM));
		    if (s.indexOf("U") == 0 && s.indexOf("T") != 1 && s.indexOf("C") != 1) break;
		}
		m_transforms.add(transform);
	    } else if (s.indexOf("Define U ") == 0) {
		int dim = 0;
		String DIM = "";
		for (int i = 9; i < s.length(); i++) {
		    if (Character.isDigit(s.charAt(i))) {
			DIM += s.charAt(i);
		    }
		}
		try {
		    dim = Integer.parseInt(DIM);
		} catch (Exception e) { handleEx(e); }
		m_U = new Matrix(dim,dim);
		for (int i = 0; i < dim; i++) {
		    try { 
			s = br.readLine(); 
		    } catch (Exception e) { handleEx(e); }
		    if (s == null) {
			System.err.println("Malformed input file.");
			System.exit(1);
		    }
		    index = s.indexOf("#");
		    if (index != -1) {
			s = s.substring(0, index);
		    }
		    m_ta.append(s+"\n");
		    int count = 0;
		    for (int j = 0; j < dim; j++) {
			String ELEM = "";
			int elem = 0;
			while (count < s.length() && !Character.isDigit(s.charAt(count))) {
			    count++;
			}
			while (count < s.length() && Character.isDigit(s.charAt(count))) {
			    ELEM += s.charAt(count);
			    count++;
			}
			try {
			    elem = Integer.parseInt(ELEM);
			    m_U.assign(i,j,elem,0.0);
			} catch (Exception e) { handleEx(e); }
		    }
		}
	    } else if (s.indexOf("Define V ") == 0) {
		int dim = 0;
		String DIM = "";
		for (int i = 9; i < s.length(); i++) {
		    if (Character.isDigit(s.charAt(i))) {
			DIM += s.charAt(i);
		    }
		}
		try {
		    dim = Integer.parseInt(DIM);
		} catch (Exception e) { handleEx(e); }
		m_V = new Matrix(dim,dim);
		for (int i = 0; i < dim; i++) {
		    try { 
			s = br.readLine(); 
		    } catch (Exception e) { handleEx(e); }
		    if (s == null) {
			System.err.println("Malformed input file.");
			System.exit(1);
		    }
		    index = s.indexOf("#");
		    if (index != -1) {
			s = s.substring(0, index);
		    }
		    m_ta.append(s+"\n");
		    int count = 0;
		    for (int j = 0; j < dim; j++) {
			String ELEM = "";
			double elem = 0;
			while (count < s.length() && !Character.isDigit(s.charAt(count)) && s.charAt(count) != '-' && s.charAt(count) != '.') {
			    count++;
			}
			while (count < s.length() && (Character.isDigit(s.charAt(count)) || s.charAt(count) == '-' || s.charAt(count) == '.')) {
			    ELEM += s.charAt(count);
			    count++;
			}
			try {
			    elem = Double.parseDouble(ELEM);
			    m_V.assign(i,j,elem,0.0);
			} catch (Exception e) { handleEx(e); }
		    }
		}
	    } else {
		System.err.println("Malformed input file.");
		System.err.println("Have a nice day.");
		System.exit(1);
	    }
	}
	try { br.close(); } catch (Exception e) { handleEx(e); }
	//if (m_U != null)
	    //System.out.print(m_U.print());
	//if (m_V != null)
	    //System.out.print(m_V.print());
	//printTransforms(m_transforms);
	m_p.setCircuitParameters(m_n, m_U, m_V, m_phi0, m_transforms);
	int dim = (int)Math.pow(2.0,(double)m_n);
	m_currentPhi = new Matrix(1,dim);
	m_measured = new Matrix(1,dim);
	m_measurements = new Matrix(1,dim);
	return;
    }

    public void printU(Vector U)
    {
	for (int i = 0; i < U.size(); i++) {
	    Vector v = (Vector)U.elementAt(i);
	    for (int j = 0; j < v.size(); j++) { 
		Integer I = (Integer)v.elementAt(j);
		System.out.print(""+I.intValue()+" ");
	    }
	    System.out.println();
	}
    }

    public void printTransforms(Vector transforms)
    {
	for (int i = 0; i < transforms.size(); i++) {
	    Vector v = (Vector)transforms.elementAt(i);
	    for (int j = 0; j < v.size(); j++) { 
		String s = (String)v.elementAt(j);
		System.out.print(s+" ");
	    }
	    System.out.println();
	}
    }

    public void printPhi(Vector phi)
    {
	for (int i = 0; i < phi.size(); i++) {
	    Integer I = (Integer)phi.elementAt(i);
	    System.out.print("|"+i+"> "+I.intValue()+" ");
	}
	System.out.println();
    }

    public void paint(Graphics g)
    {
	drawQubits(g);
    }

    public void drawQubits(Graphics g)
    {
	g.setColor(Color.black);
	g.fillRect(3, 448, 504, 244);
	for (int i = 0; i < m_currentPhi.getHeight(); i++) {
	    double real = m_currentPhi.getValue(i,0).getReal();
	    if (real >= 0.0) {
		g.setColor(Color.cyan);
	    } else {
		g.setColor(Color.magenta);
		real = -real;
	    }
	    double xrange = (double)m_currentPhi.getHeight();
	    double yrange = 1.0;
	    double x = (double)i/xrange * 500.0;
	    double h = real/yrange * 240.0;
	    double w = 500.0/xrange;
	    if (w < 1) w = 1;
	    g.fillRect((int)x+5,450,(int)w,(int)h);
	    double imaginary = m_currentPhi.getValue(i,0).getImaginary();
	    if (imaginary >= 0.0) {
		g.setColor(Color.blue);
	    } else {
		g.setColor(Color.red);
		imaginary = -imaginary;
	    }
	    xrange = (double)m_currentPhi.getHeight();
	    yrange = 1.0;
	    int realheight = (int)h;
	    x = (double)i/xrange * 500.0;
	    h = imaginary/yrange * 240.0;
	    w = 500.0/xrange;
	    g.fillRect((int)x+5,450+realheight,(int)w,(int)h);
	}
    }

    public void handleEx(Exception e) {
        System.err.println("" + e);
        e.printStackTrace();
    }

    public void setPosition(int x, int y)
    {
	//System.out.println(""+x+" "+y);
	updatePanel();
    }

    void updatePanel() {
	m_p.repaint();
    }

    public void itemStateChanged(ItemEvent e) 
    {
	updatePanel();
	repaint();
    }

    public void initializeMeasured()
    {
	for (int i = 0; i < m_measured.getHeight(); i++) {
	    m_measured.assign(i,0,0.0,0.0);
	    m_measurements.assign(i,0,0.0,0.0);
	}
    }

    public void initializePhi()
    {
	Vector matrices = new Vector();
	for (int i = 0; i < m_phi0.size(); i++) {
	    Integer I = (Integer)m_phi0.elementAt(i);
	    Matrix m = new Matrix(1,2);
	    if (I == 0) {
		m.assign(0,0,1.0,0.0);
		m.assign(1,0,0.0,0.0);
		matrices.add(m);
	    } else if (I == 1) {
		m.assign(0,0,0.0,0.0);
		m.assign(1,0,1.0,0.0);
		matrices.add(m);
	    } else {
		System.err.println("Qubits can initially be only 0 or 1.");
		System.err.println("Have a nice day.");
		System.exit(1);
	    }
	}
	while (matrices.size() > 1) {
	    Matrix m1 = (Matrix)matrices.elementAt(0);
	    Matrix m2 = (Matrix)matrices.elementAt(1);
	    Matrix bigmatrix = Matrix.combine(m1,m2);
	    matrices.setElementAt(bigmatrix,0);
	    matrices.removeElementAt(1);
	}
	m_currentPhi=(Matrix)matrices.elementAt(0);
	matrices = new Vector();
	m_ta.setText(m_currentPhi.printNonzero());
    }

    public int log2(int a)
    {
	int i = 0;
	for (int q = 1; q < a; i++, q *= 2);
	return i;
    }

    public void measure(int qubit)
    {
	double a = 0.0;
	double b = 0.0;
	int numqubits = log2(m_currentPhi.getHeight());
	int shift = numqubits-1-qubit;
	//System.err.println("Now measuring qubit "+qubit+" of "+numqubits);
	//System.err.println("Shift="+shift);
	for (int i = 0; i < m_currentPhi.getHeight(); i++) {
	    double v = m_currentPhi.getValue(i,0).getReal();
	    double w = m_currentPhi.getValue(i,0).getImaginary();
	    if (((i >> shift) & 1) == 0)
		a += v * v + w * w;
	    else if (((i >> shift) & 1) == 1)
		b += v * v + w * w;
	    else {
		System.err.println("Whoa, nellie!");
		System.exit(1);
	    }
	    //System.out.println(""+m_currentPhi.getValue(i,0)+"a="+a+"b="+b);
	}
	double d = Math.random();
	//System.out.println("d="+d);
	//System.err.println("a="+a+"b="+b);
	if (d < a)  {
	    System.out.println("Qubit "+qubit+" measured as 0");
	    m_measurements.assign(qubit,0,0.0,0.0);
	} else {
	    System.out.println("Qubit "+qubit+" measured as 1");
	    m_measurements.assign(qubit,0,1.0,0.0);
	}
	m_measured.assign(qubit,0,1.0,0.0);
	//System.out.println("Measurements:");
	//for (int i = 0; i < m_measurements.getHeight(); i++) {
	    //if (m_measured.getValue(i,0).getReal() == 1.0)
		//System.out.println(""+i+":"+m_measurements.getValue(i,0).getReal());
	//}
	
	double B = 0.0;
	for (int i = 0; i < m_currentPhi.getHeight(); i++) {
	    double v = m_currentPhi.getValue(i,0).getReal();
	    double w = m_currentPhi.getValue(i,0).getImaginary();
	    int bit = (i >> shift) & 1;
	    if (bit == 0 && d < a) 
		B += v * v + w * w;
	    if (bit == 1 && d > a) 
		B += v * v + w * w;
	    //System.out.print("B="+B);
	}
	//System.out.println();
	
	for (int i = 0; i < m_currentPhi.getHeight(); i++) {
	    double v = m_currentPhi.getValue(i,0).getReal();
	    double w = m_currentPhi.getValue(i,0).getImaginary();
	    int bit = (i >> shift) & 1;
	    //System.out.println("i="+i+":"+bit+":"+d+":"+a);
	    if (bit == 0 && d > a)
		m_currentPhi.assign(i,0,0.0,0.0);
	    else if (bit == 1 && d < a)
		m_currentPhi.assign(i,0,0.0,0.0);
	    else
		m_currentPhi.assign(i,0,v*Math.sqrt(1.0/B),w*Math.sqrt(1.0/B));
	}
	//System.err.println(m_currentPhi.print());
    }

    public void calculateNextPhi(boolean bTrace)
    {
	int dim = (int)Math.pow(2.0,(double)m_n);
	Matrix nextPhi = new Matrix(dim,1);
	Vector matrices = new Vector();
	Vector v = (Vector)m_transforms.elementAt(m_step-1);
	int start = -1;
	int ut1 = -1;
	int ut2 = -1;
	int t1 = -1;
	int t2 = -1;
	int s1 = -1;
	int cs1 = -1;
	int ucs1 = -1;
	int ct1 = -1;
	int uct1 = -1;
	int csp1 = -1;
	int ucsp1 = -1;
	int ctp1 = -1;
	int uctp1 = -1;
	int ucr41 = -1;
	int ucr4p1 = -1;
	    
	for (int k = 0; k < v.size(); k++) {
	    String s = (String)v.elementAt(k);
	    if (s.compareTo("S") == 0) {
		Matrix m = new Matrix(2,2);
		m.assign(0,0,1.0,0.0);
		m.assign(0,1,0.0,0.0);
		m.assign(1,0,0.0,0.0);
		m.assign(1,1,0.0,1.0);
		matrices.add(m);
	    } else if (s.compareTo("T") == 0) {
		Matrix m = new Matrix(2,2);
		m.assign(0,0,1.0,0.0);
		m.assign(0,1,0.0,0.0);
		m.assign(1,0,0.0,0.0);
		m.assign(1,1,0.707107,0.707107);
		matrices.add(m);
	    } else if (s.compareTo("S1") ==0) {
		s1 = k;
	    } else if (s.compareTo("S2") == 0) {
		int d1 = k - s1 + 1;
		int d2 = (int)Math.pow(2.0,(double)d1);
		Matrix m = new Matrix(d2,d2);
		for (int i = 0; i < d2; i++) {
		    for (int j = 0; j < d2; j++) {
			m.assign(i,j,0.0,0.0);
		    }
		}
		for (int i = 0; i < d2; i++) {
		    int before = i;
		    int after = i;
		    int b = i & 1;
		    int a = ((i >> (d1-1)) & 1);
		    after = 0;
		    after |= a;
		    after |= b << (d1-1);
		    for (int j = 1; j < d1-1; j++) {
			int middlebit = (before >> j) & 1;
			after |= middlebit << j;
		    }
		    m.assign(after,before,1.0,0.0);
		}
		matrices.add(m);
		s1 = -1;
	    } else if (s.compareTo("CS1") == 0) {
		cs1 = k;
	    } else if (s.compareTo("CS2") == 0) {
		int d1 = k - cs1 + 1;
		int d2 = (int)Math.pow(2.0,(double)d1);
		Matrix m = new Matrix(d2,d2);
		for (int i = 0; i < d2; i++) {
		    for (int j = 0; j < d2; j++) {
			m.assign(i,j,0.0,0.0);
		    }
		}
		for (int i = 0; i < d2; i++) {
		    int before = i;
		    int after = i;
		    int c = ((i >> (d1-1)) & 1);
		    int t = i & 1;
		    after = before;
		    if (c == 1 && t == 1)
			m.assign(after,before,0.0,1.0);
		    else
			m.assign(after,before,1.0,0.0);
		}
		matrices.add(m);
		cs1 = -1;
	    } else if (s.compareTo("UCS1") == 0) {
		ucs1 = k;
	    } else if (s.compareTo("UCS2") == 0) {
		int d1 = k - ucs1 + 1;
		int d2 = (int)Math.pow(2.0,(double)d1);
		Matrix m = new Matrix(d2,d2);
		for (int i = 0; i < d2; i++) {
		    for (int j = 0; j < d2; j++) {
			m.assign(i,j,0.0,0.0);
		    }
		}
		for (int i = 0; i < d2; i++) {
		    int before = i;
		    int after = i;
		    int t = ((i >> (d1-1)) & 1);
		    int c = i & 1;
		    after = before;
		    if (c == 1 && t == 1)
			m.assign(after,before,0.0,1.0);
		    else
			m.assign(after,before,1.0,0.0);
		}
		matrices.add(m);
		ucs1 = -1;
	    } else if (s.compareTo("CT1") == 0) {
		ct1 = k;
	    } else if (s.compareTo("CT2") == 0) {
		int d1 = k - ct1 + 1;
		int d2 = (int)Math.pow(2.0,(double)d1);
		Matrix m = new Matrix(d2,d2);
		for (int i = 0; i < d2; i++) {
		    for (int j = 0; j < d2; j++) {
			m.assign(i,j,0.0,0.0);
		    }
		}
		for (int i = 0; i < d2; i++) {
		    int before = i;
		    int after = i;
		    int c = ((i >> (d1-1)) & 1);
		    int t = i & 1;
		    after = before;
		    if (c == 1 && t == 1)
			m.assign(after,before,0.707107,0.707107);
		    else
			m.assign(after,before,1.0,0.0);
		}
		matrices.add(m);
		ct1 = -1;
	    } else if (s.compareTo("UCT1") == 0) {
		uct1 = k;
	    } else if (s.compareTo("UCT2") == 0) {
		int d1 = k - uct1 + 1;
		int d2 = (int)Math.pow(2.0,(double)d1);
		Matrix m = new Matrix(d2,d2);
		for (int i = 0; i < d2; i++) {
		    for (int j = 0; j < d2; j++) {
			m.assign(i,j,0.0,0.0);
		    }
		}
		for (int i = 0; i < d2; i++) {
		    int before = i;
		    int after = i;
		    int t = ((i >> (d1-1)) & 1);
		    int c = i & 1;
		    after = before;
		    if (c == 1 && t == 1)
			m.assign(after,before,0.707107,0.707107);
		    else
			m.assign(after,before,1.0,0.0);
		}
		matrices.add(m);
		uct1 = -1;
	    } else if (s.compareTo("UCR41") == 0) {
		ucr41 = k;
	    } else if (s.compareTo("UCR42") == 0) {
		int d1 = k - ucr41 + 1;
		int d2 = (int)Math.pow(2.0,(double)d1);
		Matrix m = new Matrix(d2,d2);
		for (int i = 0; i < d2; i++) {
		    for (int j = 0; j < d2; j++) {
			m.assign(i,j,0.0,0.0);
		    }
		}
		for (int i = 0; i < d2; i++) {
		    int before = i;
		    int after = i;
		    int t = ((i >> (d1-1)) & 1);
		    int c = i & 1;
		    after = before;
		    if (c == 1 && t == 1)
			m.assign(after,before,0.92387953251,0.38268343237);
		    else
			m.assign(after,before,1.0,0.0);
		}
		matrices.add(m);
		ucr41 = -1;
	    } else if (s.compareTo("UCR4P1") == 0) {
		ucr4p1 = k;
	    } else if (s.compareTo("UCR4P2") == 0) {
		int d1 = k - ucr4p1 + 1;
		int d2 = (int)Math.pow(2.0,(double)d1);
		Matrix m = new Matrix(d2,d2);
		for (int i = 0; i < d2; i++) {
		    for (int j = 0; j < d2; j++) {
			m.assign(i,j,0.0,0.0);
		    }
		}
		for (int i = 0; i < d2; i++) {
		    int before = i;
		    int after = i;
		    int t = ((i >> (d1-1)) & 1);
		    int c = i & 1;
		    after = before;
		    if (c == 1 && t == 1)
			m.assign(after,before,0.92387953251,-0.38268343237);
		    else
			m.assign(after,before,1.0,0.0);
		}
		matrices.add(m);
		ucr4p1 = -1;
	    } else if (s.compareTo("CSP1") == 0) {
		cs1 = k;
	    } else if (s.compareTo("CSP2") == 0) {
		int d1 = k - cs1 + 1;
		int d2 = (int)Math.pow(2.0,(double)d1);
		Matrix m = new Matrix(d2,d2);
		for (int i = 0; i < d2; i++) {
		    for (int j = 0; j < d2; j++) {
			m.assign(i,j,0.0,0.0);
		    }
		}
		for (int i = 0; i < d2; i++) {
		    int before = i;
		    int after = i;
		    int c = ((i >> (d1-1)) & 1);
		    int t = i & 1;
		    after = before;
		    if (c == 1 && t == 1)
			m.assign(after,before,0.0,-1.0);
		    else
			m.assign(after,before,1.0,0.0);
		}
		matrices.add(m);
		cs1 = -1;
	    } else if (s.compareTo("UCSP1") == 0) {
		ucs1 = k;
	    } else if (s.compareTo("UCSP2") == 0) {
		int d1 = k - ucs1 + 1;
		int d2 = (int)Math.pow(2.0,(double)d1);
		Matrix m = new Matrix(d2,d2);
		for (int i = 0; i < d2; i++) {
		    for (int j = 0; j < d2; j++) {
			m.assign(i,j,0.0,0.0);
		    }
		}
		for (int i = 0; i < d2; i++) {
		    int before = i;
		    int after = i;
		    int t = ((i >> (d1-1)) & 1);
		    int c = i & 1;
		    after = before;
		    if (c == 1 && t == 1)
			m.assign(after,before,0.0,-1.0);
		    else
			m.assign(after,before,1.0,0.0);
		}
		matrices.add(m);
		ucs1 = -1;
	    } else if (s.compareTo("CTP1") == 0) {
		ct1 = k;
	    } else if (s.compareTo("CTP2") == 0) {
		int d1 = k - ct1 + 1;
		int d2 = (int)Math.pow(2.0,(double)d1);
		Matrix m = new Matrix(d2,d2);
		for (int i = 0; i < d2; i++) {
		    for (int j = 0; j < d2; j++) {
			m.assign(i,j,0.0,0.0);
		    }
		}
		for (int i = 0; i < d2; i++) {
		    int before = i;
		    int after = i;
		    int c = ((i >> (d1-1)) & 1);
		    int t = i & 1;
		    after = before;
		    if (c == 1 && t == 1)
			m.assign(after,before,0.707107,-0.707107);
		    else
			m.assign(after,before,1.0,0.0);
		}
		matrices.add(m);
		ct1 = -1;
	    } else if (s.compareTo("UCTP1") == 0) {
		uct1 = k;
	    } else if (s.compareTo("UCTP2") == 0) {
		int d1 = k - uct1 + 1;
		int d2 = (int)Math.pow(2.0,(double)d1);
		Matrix m = new Matrix(d2,d2);
		for (int i = 0; i < d2; i++) {
		    for (int j = 0; j < d2; j++) {
			m.assign(i,j,0.0,0.0);
		    }
		}
		for (int i = 0; i < d2; i++) {
		    int before = i;
		    int after = i;
		    int t = ((i >> (d1-1)) & 1);
		    int c = i & 1;
		    after = before;
		    if (c == 1 && t == 1)
			m.assign(after,before,0.707107,-0.707107);
		    else
			m.assign(after,before,1.0,0.0);
		}
		matrices.add(m);
		uct1 = -1;
	    } else if (s.compareTo("T1") == 0) {
		t1 = k;
	    } else if (s.compareTo("T2") == 0) {
		t2 = k;
	    } else if (s.compareTo("T3") == 0) {
		int d1 = k - t1 + 1;
		int d2 = (int)Math.pow(2.0,(double)d1);
		Matrix m = new Matrix(d2,d2);
		for (int i = 0; i < d2; i++) {
		    for (int j = 0; j < d2; j++) {
			m.assign(i,j,0.0,0.0);
		    }
		}
		for (int i = 0; i < d2; i++) {
		    int before = i;
		    int after = i;
		    int t = i & 1;
		    int c1 = ((i >> (d1-1)) & 1);
		    int c2 = ((i >> (k - t2)) & 1);
		    if (c1 == 0 || c2 == 0) {
			after = before;
		    } else if (c1 == 1 && c2 == 1) {
			after = before ^ 1;
		    }
		    m.assign(after,before,1.0,0.0);
		}
		matrices.add(m);
		t1 = -1;
		t2 = -1;
	    } else if (s.compareTo("UT1") == 0) {
		ut1 = k;
	    } else if (s.compareTo("UT2") == 0) {
		ut2 = k;
	    } else if (s.compareTo("UT3") == 0) {
		int d1 = k - ut1 + 1;
		int d2 = (int)Math.pow(2.0,(double)d1);
		Matrix m = new Matrix(d2,d2);
		for (int i = 0; i < d2; i++) {
		    for (int j = 0; j < d2; j++) {
			m.assign(i,j,0.0,0.0);
		    }
		}
		for (int i = 0; i < d2; i++) {
		    int before = i;
		    int after = i;
		    int c2 = i & 1;
		    int t = ((i >> (d1-1)) & 1);
		    int c1 = ((i >> (k - ut2)) & 1);
		    if (c1 == 0 || c2 == 0) {
			after = before;
		    } else if (c1 == 1 && c2 == 1) {
			after = before ^ (1<<(d1-1));
		    }
		    m.assign(after,before,1.0,0.0);
		}
		matrices.add(m);
		ut1 = -1;
		ut2 = -1;
	    } else if (s.compareTo("Control") == 0) {
		if (start != -1) {
		    System.err.println("Yikes this gate has two control bits.");
		    System.err.println("This feature is currently not supported.");
		    System.err.println("Have a nice day.");
		    System.exit(1);
		}
		start = k;
	    } else if (s.compareTo("Target") == 0) {
		if (start == -1) {
		    System.err.println("Malformed input file.");
		    System.err.println("Have a nice day.");
		    System.exit(1);
		}
		// This is just a plain vanilla CNOT gate.
		int d1 = k - start + 1;
		int d2 = (int)Math.pow(2.0,(double)d1);
		Matrix m = new Matrix(d2,d2);
		for (int i = 0; i < d2; i++) {
		    for (int j = 0; j < d2; j++) {
			m.assign(i,j,0.0,0.0);
		    }
		}
		for (int i = 0; i < d2; i++) {
		    int before = i;
		    int after = i;
		    int c = ((i >> (d1-1)) & 1);
		    int t = i & 1;
		    if (c == 0) {
			after = before;
		    } else if (c == 1) {
			after = before ^ 1;
		    }
		    m.assign(after,before,1.0,0.0);
		}
		matrices.add(m);
		start = -1;
	    } else if (s.compareTo("U") == 0) {
		matrices.add(m_U);
	    } else if (s.compareTo("V") == 0) {
		matrices.add(m_V);
	    } else if (s.compareTo("I") == 0 && start == -1 && ut1 == -1 && s1 == -1 && t1 == -1 && cs1 == -1 && ucs1 == -1 && ct1 == -1 && uct1 == -1 && csp1 == -1 && ucsp1 == -1 && ctp1 == -1 && uctp1 == -1 && ucr41 == -1 && ucr4p1 == -1) {
		Matrix m = new Matrix(2,2);
		m.assign(0,0,1.0,0.0);
		m.assign(0,1,0.0,0.0);
		m.assign(1,0,0.0,0.0);
		m.assign(1,1,1.0,0.0);
		matrices.add(m);
	    } else if (s.compareTo("X") == 0) {
		Matrix m = new Matrix(2,2);
		m.assign(0,0,0.0,0.0);
		m.assign(0,1,1.0,0.0);
		m.assign(1,0,1.0,0.0);
		m.assign(1,1,0.0,0.0);
		matrices.add(m);
	    } else if (s.compareTo("Y") == 0) {
		Matrix m = new Matrix(2,2);
		m.assign(0,0,0.0,0.0);
		m.assign(0,1,0.0,-1.0);
		m.assign(1,0,0.0,1.0);
		m.assign(1,1,0.0,0.0);
		matrices.add(m);
	    } else if (s.compareTo("Z") == 0) {
		Matrix m = new Matrix(2,2);
		m.assign(0,0,1.0,0.0);
		m.assign(0,1,0.0,0.0);
		m.assign(1,0,0.0,0.0);
		m.assign(1,1,-1.0,0.0);
		matrices.add(m);
	    } else if (s.compareTo("H") == 0) {
		Matrix m = new Matrix(2,2);
		m.assign(0,0,0.707106781186548,0.0);
		m.assign(0,1,0.707106781186548,0.0);
		m.assign(1,0,0.707106781186548,0.0);
		m.assign(1,1,-0.707106781186548,0.0);
		matrices.add(m);
	    } else if (s.compareTo("M") == 0) {
		measure(k);
		Matrix m = new Matrix(2,2);
		m.assign(0,0,1.0,0.0);
		m.assign(0,1,0.0,0.0);
		m.assign(1,0,0.0,0.0);
		m.assign(1,1,1.0,0.0);
		matrices.add(m);
	    } else if (s.compareTo("CNOT") == 0) {
		Matrix m = new Matrix(4,4);
		m.assign(0,0,1.0,0.0);
		m.assign(0,1,0.0,0.0);
		m.assign(0,2,0.0,0.0);
		m.assign(0,3,0.0,0.0);
		m.assign(1,0,0.0,0.0);
		m.assign(1,1,1.0,0.0);
		m.assign(1,2,0.0,0.0);
		m.assign(1,3,0.0,0.0);
		m.assign(2,0,0.0,0.0);
		m.assign(2,1,0.0,0.0);
		m.assign(2,2,0.0,0.0);
		m.assign(2,3,1.0,0.0);
		m.assign(3,0,0.0,0.0);
		m.assign(3,1,0.0,0.0);
		m.assign(3,2,1.0,0.0);
		m.assign(3,3,0.0,0.0);
		matrices.add(m);
	    } else if (start == -1 && ut1 == -1 && s1 == -1 && t1 == -1 && cs1 == -1 && ucs1 == -1 && ct1 == -1 && uct1 == -1 && csp1 == -1 && ucsp1 == -1 && ctp1 == -1 && uctp1 == -1 && ucr41 == -1 && ucr4p1 == -1) {
		System.err.println(s+": No such quantum gate.");
		System.err.println("Have a nice day.");
		System.exit(1);
	    }
	}
	while (matrices.size() > 1) {
	    Matrix m1 = (Matrix)matrices.elementAt(0);
	    Matrix m2 = (Matrix)matrices.elementAt(1);
	    //System.out.println("####");
	    //System.out.println(m1.print());
	    //System.out.println(m2.print());
	    //System.out.println("!!!!!");
	    Matrix bigmatrix = Matrix.combine(m1,m2);
	    matrices.setElementAt(bigmatrix,0);
	    matrices.removeElementAt(1);
	}
	Matrix transform = (Matrix)matrices.elementAt(0);
	nextPhi = Matrix.multiply(transform,m_currentPhi);
	m_currentPhi = nextPhi;
	m_ta.setText(nextPhi.printNonzero());
	//m_ta.append("=================\n");
	//m_ta.append(transform.print(false));

	if (bTrace) {
	    try { 
		BufferedWriter bw = new BufferedWriter(new FileWriter(m_fn+"_"+m_fileNumber+".out"));
		bw.write(nextPhi.print());
		bw.write("=================\n");
		bw.write(transform.print(false));
		bw.close();
		m_fileNumber++;
	    } catch (Exception e) {
		handleEx(e);
	    }
	}
    }

    public void actionPerformed(ActionEvent e)
    {
	if (e.getSource() == m_buttonStep) {
	    //System.out.println("Next");
	    if (m_step >= m_transforms.size()) {
		System.err.println("There are no more steps.");
		return;
	    }
	    m_step++;
	    m_p.setStep(m_step);
	    calculateNextPhi(false);
	    updatePanel();
	    repaint();
	} else if (e.getSource() == m_buttonAuto) {
	    autopilot();
	}
    }

    public void autopilot()
    {
	if (m_fileNumber == 0) {
	    try { 
		BufferedWriter bw = new BufferedWriter(new FileWriter(m_fn+"_"+m_fileNumber+".out"));
		bw.write(m_currentPhi.print());
		bw.close();
		m_fileNumber++;
	    } catch (Exception e) {
		handleEx(e);
	    }
	}
	while (m_step < m_transforms.size()) {
	    m_step++;
	    m_p.setStep(m_step);
	    calculateNextPhi(true);
	    updatePanel();
	    repaint();
	}
    }

    public void mouseClicked(MouseEvent e)
    {
	if (e.getSource() instanceof qpanel) {
	    setPosition(e.getX(), e.getY());
	}
    }

    public void mouseEntered(MouseEvent e)
    {
    }
    
    public void mouseExited(MouseEvent e)
    {
    }

    public void mousePressed(MouseEvent e)
    {
    }

    public void mouseReleased(MouseEvent e)
    {
    }
}

public class simulator {
    public static void main(String args[])
    {
	if (args.length != 1) {
	    System.err.println("Usage: java simulator circuit_file");
	    return;
	}
	qframe f = new qframe(args[0]);
	f.setVisible(true);
    }
}
