##
#  This file contains unittests for the DYPL Ruby assignment. All
#  assigments handed in must pass these tests or be failed. We
#  will then scrutinize your code to judge its quality.
#
#  Unsurprisingly, more elegant solutions will receive a higher
#  mark. Examples of elegant things include not wasting memory or
#  CPU, intelligent solutions and observations properly exploited
#  to make the code e.g., shorter, easily maintained and
#  extendable. An example of an unelegant thing is to implement
#  select_first as returning the first element of select_all.
##

require 'test/unit'
require 'yaml'

##----------------------------------------------------------------------------------

class Array
  def dd(other)
    return false unless other.kind_of? Array
    return false unless other.size == self.size
    return self.all? { |e| other.include?( e ) }
  end
end

class TestPerson
  attr_accessor :name, :age
  def initialize(name, age)
    @name, @age = name, age
  end
  def <=>(other); @age <=> other.age; end
  def inspect
    "#{@name}(#{@age})"
  end
end


class ArrayTest < Test::Unit::TestCase
  def setup
    load 'array_extension.rb'
    @johan = TestPerson.new('Johan', 26)
    @tobias = TestPerson.new('Tobias', 29)
    @beatrice = TestPerson.new('Beatrice', 32)
    @tobias_again = TestPerson.new('Tobias', -29)
    @array = [@johan, @tobias, @beatrice, @tobias_again]  
  end
  
  def teardown
  end

  def test_select_first
    assert_equal( @tobias, @array.select_first( :name => 'Tobias' ) )
    assert_equal( @johan, @array.select_first( :name => ['Tobias', 'Johan'] ) )
    assert_equal( @beatrice, @array.select_first( :name => :age, :interval => { :min => 30, :max => 32 } ) )
    assert_equal( @johan, @array.select_first( :name => :age, :interval => { :max => 32 } ) )
  end

  def test_select_all
    assert_equal( [@tobias, @tobias_again], @array.select_all( :name => 'Tobias' ) )
    assert_equal( [@johan, @tobias, @tobias_again], @array.select_all( :name => ['Tobias', 'Johan'] ) )
    assert_equal( [@beatrice], @array.select_all( :name => :age, :interval => { :min => 30, :max => 32 } ) )
    assert_equal( @array, @array.select_all( :name => :age, :interval => { :max => 32 } ) )
  end

  def test_select_first_where_name_is
    assert_equal( false, @array.methods.include?(:select_first_where_name_is), 
		 "Possible cheating? select_first_where_name_is exists in Array")
    assert_equal( @tobias, @array.select_first_where_name_is( 'Tobias' ) )
    assert( @array.methods.include?(:select_first_where_name_is), 
	   "select_first_where_name_is not added to Array after first use" )
    assert_equal( @johan, @array.select_first_where_name_is( ['Tobias', 'Johan'] ))
  end

  def test_select_first_where_age_is_in
    assert_equal( false, @array.methods.include?(:select_first_where_age_is_in),
		 "Possible cheating? select_first_where_age_is_in exists in Array")
    assert_equal( @beatrice, @array.select_first_where_age_is_in( 30, 32 ) )
    assert(@array.methods.include?(:select_first_where_age_is_in),
	   "select_first_where_age_is_in not added to Array after first use")
  end

  def test_select_all_where_name_is
    assert_equal( false, @array.methods.include?(:select_all_where_name_is),
		 "Possible cheating? select_all_where_name_is exists in Array")
    assert_equal( [@tobias, @tobias_again], @array.select_all_where_name_is( 'Tobias' ) )
    assert(@array.methods.include?(:select_all_where_name_is),
	   "select_first_where_name_is not added to Array after first use")
    assert_equal( [@johan, @tobias, @tobias_again], @array.select_all_where_name_is( ['Tobias', 'Johan'] ) )
    assert_equal( [], @array.select_all_where_name_is( ['FauxJohan', 'FauxBeatrice'] ) )
    assert_equal( [], @array.select_all_where_name_is( 'Marve Flexnes' ) )
  end
end