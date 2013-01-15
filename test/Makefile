JAVASOURCES = $(shell find . -name '*.java')
JAVABASES = $(basename $(JAVASOURCES))
JAVACLASSES = $(addsuffix .class,$(basename $(JAVASOURCES)))


java: $(JAVACLASSES)

%.class: %.java ../scijava-roi.jar
	@echo JAVAC $<
	@CLASSPATH= javac -classpath ../scijava-roi.jar -Xlint $<

test: java
	$(MAKE) $(JAVABASES)

%: %.class
	@echo JAVA $@
	@CLASSPATH= java -classpath ../scijava-roi.jar:. $@

clean:
	rm *.class

.PHONY: java clean