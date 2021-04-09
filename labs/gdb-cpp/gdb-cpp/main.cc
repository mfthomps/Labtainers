// main.cc
// Andrew Gilpin
// agg1@cec.wustl.edu

// This file contains the example program used in the gdb debugging
// tutorial. The tutorial can be found on the web at
// http://students.cec.wustl.edu/~agg1/tutorial/

#include <iostream>

int number_instantiated = 0;

template <class T>
class Node {
public:
  Node (const T &value, Node<T> *next = 0) : value_(value), next_(next) {
    std::cout << "Creating Node, "
         << ++number_instantiated
         << " are in existence right now" << std::endl;
  }
  ~Node () {
    std::cout << "Destroying Node, "
         << --number_instantiated
         << " are in existence right now" << std::endl;
    next_ = 0;
  }

  Node<T>* next () const { return next_; }
  void next (Node<T> *new_next) { next_ = new_next; };
  const T& value () const { return value_; }
  void value (const T &value) { value_ = value; }

private:
  Node ();
  T value_;
  Node<T> *next_;
};
  
template <class T>
class LinkedList {
public:
  LinkedList () : head_(0) {};
  ~LinkedList () { delete_nodes (); };

  // returns 0 on success, -1 on failure
  int insert (const T &new_item) {
    return ((head_ = new Node<T>(new_item, head_)) != 0) ? 0 : -1;
  }

  // returns 0 on success, -1 on failure
  int remove (const T &item_to_remove) {
    Node<T> *marker = head_;
    Node<T> *temp = 0;  // temp points to one behind as we iterate

    while (marker != 0) {
      if (marker->value() == item_to_remove) {
        if (temp == 0) { // marker is the first element in the list
          if (marker->next() == 0) {
            head_ = 0;
            delete marker; // marker is the only element in the list
            marker = 0;
          } else {
            head_ = new Node<T>(marker->value(), marker->next());
            delete marker;
            marker = 0;
          }
          return 0;
        } else {
          temp->next (marker->next());
          delete temp;
          temp = 0;
          return 0;
        }
      }
      marker = 0;  // reset the marker
      temp = marker;
      marker = marker->next();
    }

    return -1;	// failure
  }

  void print (void) {
    Node<T> *marker = head_;
    while (marker != 0) {
      std::cout << marker->value() << std::endl;
      marker = marker->next();
    }
  }

private:
  void delete_nodes (void) {
    Node<T> *marker = head_;
    while (marker != 0) {
      Node<T> *temp = marker;
      delete marker;
      marker = temp->next();
    }
  }
        
  Node<T> *head_;
};

int main (int argc, char **argv) {
  LinkedList<int> *list = new LinkedList<int> ();

  list->insert (1);
  list->insert (2);
  list->insert (3);
  list->insert (4);

  std::cout << "The fully created list is:" << std::endl;
  list->print ();

  std::cout << std::endl << "Now removing elements:" << std::endl;
  list->remove (4);
  list->print ();
  std::cout << std::endl;

  list->remove (1);
  list->print ();
  std::cout << std::endl;

  list->remove (2);
  list->print ();
  std::cout << std::endl;

  list->remove (3);
  list->print ();

  delete list;

  return 0;
}
