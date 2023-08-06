<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl" xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xd tei" version="1.0">

    <xsl:output indent="yes"/>

    <xd:doc scope="stylesheet">
        <xd:desc>
            <xd:p><xd:b>Created on:</xd:b> Jan 8, 2021</xd:p>
            <xd:p><xd:b>Author:</xd:b> cwulfman</xd:p>
            <xd:p/>
        </xd:desc>
    </xd:doc>

    <xsl:template match="/">
        <interview>
            <identifier>
                <xsl:value-of select="//tei:idno[@type = 'DDHI']"/>
            </identifier>
            <title>
                <xsl:value-of select="//tei:teiHeader/tei:fileDesc/tei:titleStmt"/>
            </title>
            <primary_audio_URI>
                <xsl:apply-templates select="//tei:recording[@xml:id = 'primary_recording']"/>
            </primary_audio_URI>
            <interview_body>
                <xsl:apply-templates select="tei:TEI/tei:text/tei:body"/>
            </interview_body>
            <participants>
                <xsl:apply-templates select="tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc"/>
            </participants>
            <named_persons>
                <xsl:apply-templates select="tei:TEI/tei:standOff/tei:listPerson"/>
            </named_persons>
            <named_places>
                <xsl:apply-templates select="tei:TEI/tei:standOff/tei:listPlace"/>
            </named_places>
            <named_events>
                <xsl:apply-templates select="tei:TEI/tei:standOff/tei:listEvent"/>
            </named_events>
            <named_orgs>
                <xsl:apply-templates select="tei:TEI/tei:standOff/tei:listOrg"/>
            </named_orgs>
        </interview>

    </xsl:template>

    <xsl:template match="tei:body">
        <xsl:apply-templates select="tei:u"/>
    </xsl:template>

    <xsl:template match="tei:particDesc">
        <xsl:apply-templates select="tei:person"/>
    </xsl:template>

    <xsl:template match="tei:person[ancestor::tei:particDesc]">
        <participant>
            <name>
                <xsl:value-of select="tei:persName"/>
            </name>
            <role>
                <xsl:value-of select="@role"/>
            </role>
        </participant>
    </xsl:template>
    
    <xsl:template match="tei:idno[ancestor::tei:standOff]">
        <id type="{@type}">
            <xsl:apply-templates />
        </id>
    </xsl:template>

    <xsl:template match="tei:person[ancestor::tei:standOff]">
      <person id="{@xml:id}">
        <name>
          <xsl:value-of select="tei:persName"/>
        </name>
        <xsl:apply-templates select="tei:idno" />
      </person>
    </xsl:template>

    <xsl:template match="tei:place[ancestor::tei:standOff]">
      <place id="{@xml:id}">
        <name>
            <xsl:value-of select="tei:placeName"/>
        </name>
        <xsl:apply-templates select="tei:idno" />
      </place>
    </xsl:template>

    <xsl:template match="tei:org[ancestor::tei:standOff]">
      <org id="{@xml:id}">
        <name>
	  <xsl:value-of select="tei:orgName"/>
	</name>
        <xsl:apply-templates select="tei:idno" />
        </org>
    </xsl:template>

    <xsl:template match="tei:event[ancestor::tei:standOff]">
        <event id="{@xml:id}">
	  <name>
            <xsl:value-of select="tei:desc"/>
	  </name>
          <xsl:apply-templates select="tei:idno" />
        </event>
    </xsl:template>

    <xsl:template match="tei:u">
        <dl>
            <dt>
                <span data-id-type="DDHI" data-id="{@who}">
                    <xsl:value-of select="string(@who)"/>
                </span>
            </dt>
            <dd>
                <xsl:apply-templates/>
            </dd>
        </dl>
    </xsl:template>

    <xsl:template match="tei:persName[ancestor::tei:u] | 
        tei:placeName[ancestor::tei:u] |
        tei:orgName[ancestor::tei:u] | 
        tei:name[@type='event' and ancestor::tei:u]"
        >
        <span data-id-type="DDHI" data-id="{substring-after(@ref, '#')}">
            <xsl:apply-templates/>
        </span>
    </xsl:template>
</xsl:stylesheet>
